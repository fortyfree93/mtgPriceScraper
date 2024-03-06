import requests
from bs4 import BeautifulSoup
import re

class Proxy():
    # Regular expression pattern to match IP addresses with port numbers
    regex = r"[0-9]+(?:\.[0-9]+){3}:[0-9]+"
    _proxy_list = []

    def __init__(self, mode:str, export_to_file:bool=False) -> None:
        self.__load_proxies(mode=mode,export_to_file=export_to_file)

    def __load_proxies(self, mode:str, export_to_file:bool=False):
        # Switch based on the mode provided
        match mode:
            # If the mode is 'spys', scrape proxies from spys.me
            case 'spys':
                result = requests.get("https://spys.me/proxy.txt")
                test_str = result.text
                a = re.finditer(self.regex, test_str, re.MULTILINE)                

                # Extract proxies using regular expressions and add them to proxy_list
                for i in a:
                    # Adjust the format of the proxy list to http://<ip>:<port>/
                    self._proxy_list.append(f"http://{i.group()}/")

            # If the mode is 'fpl', scrape proxies from free-proxy-list.net
            case 'fpl':
                result = requests.get("https://free-proxy-list.net/")
                soup = BeautifulSoup(result.content, 'html.parser')
                # Find the textarea containing proxies in the HTML
                z = soup.find('textarea').get_text()
                # Extract proxies using regular expressions and add them to proxy_list
                x = re.findall(self.regex, z)
                for i in x:
                    # Adjust the format of the proxy list to http://<ip>:<port>/
                    self._proxy_list.append(f"http://{i}/")

            # If the mode is 'file', load proxies from a file
            case 'file':
                # Load proxies from a previously written file
                with open("proxies_list.txt", "r") as file:
                    for line in file:
                        # Strip any leading or trailing whitespace and add the proxy to proxy_list
                        self._proxy_list.append(line.strip())    

        # If export_to_file is True, write the proxies to a file
        if export_to_file == True:
            with open("proxies_list.txt", "w") as myfile:
                for line in self._proxy_list:
                    # Write each proxy to the file
                    print(line, file=myfile)                        
    
    def get_proxies(self):
        return self._proxy_list

    def test_proxies(self):
        working_proxies = []
        for proxy in self._proxy_list:
            try:
                response = requests.get("http://google.at", proxies={"http": proxy}, timeout=200)
                if response.status_code == 200:
                    working_proxies.append(proxy)
                    print(f"Proxy {proxy} is working.")
            except Exception as e:
                print(f"Proxy {proxy} is not working: {e}")
        return working_proxies