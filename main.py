import proxy, argparse, csv, requests, logging, time
from random_header_generator import HeaderGenerator
from mtg_single_parser import Mtg_single_parser
from mtgcard import Card

import concurrent.futures
from tqdm import tqdm

def fetch_price_with_proxy(card:Card, proxy: str):
    # set formatted field velus for set_name & name
    card.set_formattet_field_values()
    url = f'https://www.cardmarket.com/en/Magic/Products/Singles/{card.formatted_set_name}/{card.formatted_card_name}'    

    logger.debug(f"{card.set_name}/{card.name} request (via {proxy}): {url}")

    # generate randomized http headers
    http_headers = header_generator()  
    http_headers['Accept-Language'] = 'en-US,en;q=0.5'
    http_headers['Accept-Encoding'] = "gzip, deflate;q=0.7, identity;q=0.4'1"
    http_headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'    

    try:
        response = requests.get(url, headers=http_headers, proxies={"http": proxy}, timeout=10)    

        logger.debug(f"http satus: {response.status_code}")

        if response.status_code == 200: 
            #parse html result and set pricing details on card object      
            mtg_single_parser = Mtg_single_parser(response.text)
            if mtg_single_parser.error_msg != None:
                card.error = True
                # errors thrown on cardmarket website
                logger.info(f"retrieved price details: {mtg_single_parser.error_msg}")
                return f"Failed to fetch data for {url} (via {proxy}: {mtg_single_parser.error_msg})"     
                       
            card.set_price_details(mtg_single_parser.price_details)
            card.set_timestamp()

            logger.debug(f"retrieved price details: {mtg_single_parser.price_details}")
        else:
            return f"Failed to fetch data for {url} (via {proxy})"
    except Exception as e:
        return f"Error occurred for {card.name} (via {proxy}): {str(e)}  url = {url}"

def scrape_card_prices_with_proxies(card_list, proxy_lst, args):
    """
    Scrapes the price details for a list of cards using a list of proxies in single tasks.

    Args:
        card_list (list): A list of Card objects to scrape prices for.
        proxy_lst (list): A list of proxies to use for the requests.
        args: Command-line arguments parsed using argparse.

    Returns:
        list: A list of messages indicating success or failure for each card.
    """
    results = []
    num_proxies = len(proxy_lst)
    proxy_index = 0  # Initialize the index of the current proxy
    
    for card in card_list:
        if args.init and card.is_price_details_init():
            # skip if only init is requested
            logger.debug(f"skiped: {card.set_name}/{card.name}")

            global cnt_complete
            cnt_complete += 1

            continue 

        proxy = proxy_lst[proxy_index]  # Get the current proxy
        result = fetch_price_with_proxy(card, proxy)
        results.append(result)
        
        # Move to the next proxy index (cycling back to 0 if needed)
        proxy_index = (proxy_index + 1) % num_proxies
    
    return results

def scrape_card_prices_with_proxies_mp(card_list, proxy_lst, args):
    """
    Scrapes the price details for a list of cards using a list of proxies in multiple tasks.

    Args:
        card_list (list): A list of Card objects to scrape prices for.
        proxy_lst (list): A list of proxies to use for the requests.
        args: Command-line arguments parsed using argparse.

    Returns:
        list: A list of messages indicating success or failure for each card.
    """

    results = []
    num_proxies = len(proxy_lst)

    # Create a progress bar
    progress_bar = tqdm(total=len(card_list), desc="Fetching prices", unit="cards")

    def fetch_price(card, proxy):
        nonlocal progress_bar
        result = fetch_price_with_proxy(card, proxy)
        results.append(result)
        # Update the progress bar
        progress_bar.update(1)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for card in card_list:
            if args.init and card.is_price_details_init():
                # skip if only init is requested
                logger.debug(f"Skipped: {card.set_name}/{card.name}")
                progress_bar.update(1)
                
                # count initialized cases
                global cnt_complete
                cnt_complete += 1

                continue

            proxy = proxy_lst[num_proxies % len(proxy_lst)]  # Get the current proxy
            futures.append(executor.submit(fetch_price, card, proxy))
            num_proxies += 1

        # Wait for all tasks to complete
        concurrent.futures.wait(futures)

    # Close the progress bar
    progress_bar.close()

    return results

def read_cards_list(filename):    
    with open(filename, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # create card object                                                
            card = Card(
                row.get('Name', ''),
                row.get('Set code', ''),
                row.get('Set name', ''),
                row.get('Collector number', ''),
                row.get('Foil', ''),
                row.get('Rarity', ''),
                row.get('Quantity', ''),
                row.get('ManaBox ID', ''),
                row.get('Scryfall ID', ''),
                row.get('Purchase price', ''),
                row.get('Misprint', ''),
                row.get('Altered', ''),
                row.get('Condition', ''),
                row.get('Language', ''),
                row.get('Purchase price currency', ''),
                row.get('last update', ''),
                row.get('Error', False)
            )

            # fill price details, if available
            price_details = {}
            price_details['available'] = row.get('Available items', None)
            price_details['price_avg_30'] = row.get('30-days average price', None)
            price_details['price_avg_7'] = row.get('7-days average price', None)
            price_details['price_avg_1'] = row.get('1-day average price', None)
            price_details['price_from'] = row.get('Price from', None)
            price_details['price_trend'] = row.get('Price trend', None)
            card.set_price_details(price_details)

            card_list.append(card)

def write_cards_to_csv(filename):   
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(['Name', 'Set code', 'Set name', 'Collector number', 'Foil', 'Rarity', 'Quantity',
                         'ManaBox ID', 'Scryfall ID', 'Purchase price', 'Misprint', 'Altered', 'Condition',
                         'Language', 'Purchase price currency',
                         'Available items', 'Price from', 'Price trend', '30-days average price',
                         '7-days average price', '1-day average price', 'last update','error'])
        # Write data for each card
        for card in card_list:
            writer.writerow([card.name, card.set_code, card.set_name, card.collector_number, card.foil, card.rarity,
                             card.quantity, card.mana_box_id, card.scryfall_id, card.purchase_price, card.misprint,
                             card.altered, card.condition, card.language, card.purchase_price_currency,
                             card.price_details['available'],
                             card.price_details['price_from'],
                             card.price_details['price_trend'],
                             card.price_details['price_avg_30'],
                             card.price_details['price_avg_7'],
                             card.price_details['price_avg_1'],
                             card.last_update,
                             card.error ])

def parse_args():
    # declare command line arguements
    parser = argparse.ArgumentParser(description="Scrape prices from Cardmarket!")   
    parser.add_argument('-i','--init', action='store_true', dest='init', help="only process initial lines (without timestamp)")
    parser.add_argument('-f','--file-in',type=str, dest='file_in', help="path to intput file")
    parser.add_argument('-o','--file-out', type=str, dest='file_out', help="path to output file")
    parser.add_argument("-p", "--proxy-mode", choices=["spys", "fpl", "file"],dest='proxy_mode', default="spys", help="Proxy retrieval mode")
    
    args, unknown = parser.parse_known_args()

    if unknown:
        raise ValueError(f"Unknown arguments: {unknown}")
    
    if args.file_in == None:
        raise ValueError (f"No file parsed")
    
    if args.file_out == None:
        # same file for in and output
        args.file_out = args.file_in

    return args    

#---------------------------------------------------------------------------

# Create logger
logger = logging.getLogger('CM-MTG-Price-Scraper')
logger.setLevel(logging.DEBUG)

# Create file handler and set level to debug
fh = logging.FileHandler('app.log')
fh.setLevel(logging.DEBUG)

# Create console handler and set level to error
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# Create formatter and set it to both handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(fh)
logger.addHandler(ch)

global cnt_complete #counter for completed init/update
cnt_complete = 0

try:
    args = parse_args()    
    logger.info(f"Starting wiht params: {args}")

    card_list = []
    # read cards form given .csv file
    read_cards_list(args.file_in)
    logger.info(f"Retrieved items from .csv: {len(card_list)}")    

    # init list of proxies
    proxy = proxy.Proxy(mode=args.proxy_mode, export_to_file=True)
    proxy_list = proxy.get_proxies()
    logger.info(f"Proxies retrieved (mode = {args.proxy_mode}): {len(proxy_list)}")

    # init http header generator
    header_generator = HeaderGenerator(user_agents = 'scrape')    

    mtg_single_parser = Mtg_single_parser()   

    while cnt_complete < len(card_list):
        # do the actual magic
        cnt_complete = 0
        #results = scrape_card_prices_with_proxies(card_list, proxy_list, args)
        results = scrape_card_prices_with_proxies_mp(card_list, proxy_list, args)

        write_cards_to_csv(args.file_out)
        logger.info(f"Completed cards: {cnt_complete}")
        
        # Wait
        time.sleep(10)

except Exception as e:    
    logger.error(str(e))