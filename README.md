# Magic The Gathering - Cardmarket Price Scraper

## Introduction
This application scrapes price details for Magic: The Gathering cards from Cardmarket using proxies and stores the data in a CSV file.

Pricing source: https://www.cardmarket.com/en
Free proxy sources: https://spys.me/, https://free-proxy-list.net/

## Installation
To use this application, follow these steps:

1. Clone the repository: `git clone https://github.com/your-username/mtg-price-scraper.git`
2. Navigate to the project directory: `cd mtg-price-scraper`
3. Install dependencies: `pip install -r requirements.txt`

## Logging
Log files are stored in the **app.log**-File. You can view the log files to monitor the application's activity and diagnose any issues.

## Usage
### Running the Application
To run the application, use the following command:

```sh
python main.py [-h] [-i] [-fi FILE_IN] [-fo FILE_OUT]
```
### Command line
show help
```sh
urate@uRate:~/datafetcher$ python main.py -h
```
output:
```sh
usage: main.py [-h] [-c] [-token TOKEN] [-api {av,eod,yf}]

options:
  -h, --help            show this help message and exit
  -i, --init            only process initial lines (without timestamp)
  -f FILE_IN, --file-in FILE_IN
                        path to intput file
  -o FILE_OUT, --file-out FILE_OUT
                        path to output file
  -p {spys,fpl,file}, --proxy-mode {spys,fpl,file}
                        Proxy retrieval mode
```