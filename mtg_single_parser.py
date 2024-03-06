from bs4 import BeautifulSoup

class Mtg_single_parser():

    price_details = {}
    listings = []

    def __init__(self, raw_html=None) -> None:        
        self.__reset_details()

        if raw_html != None:
            self.raw_html = raw_html
            self.__retrieve_details()            

    def __reset_details(self):
        self.price_details = {
            'available': 0,
            'price_from': 0.0,
            'price_trend': 0.0,
            'price_avg_30': 0.0,
            'price_avg_7': 0.0,
            'price_avg_1': 0.0
        }  

    def __retrieve_details(self):
        self.__reset_details()
                
        soup = BeautifulSoup(self.raw_html, 'html.parser')
        
        details_table = soup.find(class_='labeled row mx-auto g-0')

        # Extract data from the HTML        
        for dt, dd in zip(soup.find_all('dt'), soup.find_all('dd')):
            key = dt.text.strip()
            value = dd.text.strip()
            
            self.__details_data_mapping(key, value)
    
    def __details_data_mapping(self, raw_field, raw_value):        
        match raw_field:
            case 'Available items':
                self.price_details['available'] = raw_value
            case 'From':
                self.price_details['price_from'] = self.__interpret_price_values(raw_value)
            case 'Price Trend':
                self.price_details['price_trend'] = self.__interpret_price_values(raw_value)
            case '30-days average price':
                self.price_details['price_avg_30'] = self.__interpret_price_values(raw_value)
            case '7-days average price':
                self.price_details['price_avg_7'] = self.__interpret_price_values(raw_value)
            case '1-day average price':
                self.price_details['price_avg_1'] = self.__interpret_price_values(raw_value)
    
    def __interpret_price_values(self, price_str) -> float:
        # Remove euro symbol and commas
        price_str = price_str.replace("€", "").replace(".", "").replace(",", ".")

        # Convert to float and round to two decimal places
        price_float = round(float(price_str), 2)
        return price_float

    def __retrieve_listings(self, raw_html):
        #TODO: retrieve listings from raw html
        soup = BeautifulSoup(raw_html, 'html.parser')

        # Extracting seller info
        seller_info = soup.find(class_='seller-info')
        sell_count = seller_info.find(class_='sell-count').text
        item_location = seller_info.find(class_='icon')['title'].split(':')[-1].strip()
        seller_name = seller_info.find('a').text.strip()

        # Extracting product info
        product_info = soup.find(class_='col-product')
        item_condition = product_info.find(class_='article-condition').text.strip()
        price = product_info.find(class_='color-primary').text.strip()

        # Extracting offer info
        offer_info = soup.find(class_='col-offer')
        quantity = offer_info.find(class_='item-count').text.strip()

        # Storing data in array
        row_data = [sell_count, item_location, seller_name, item_condition, price, quantity]

        print(row_data)
