## Scrape Stock Prices from Yahoo Finance with Python
# Manual scrape if API does not cover what we need; writes to csv file

import requests
from bs4 import BeautifulSoup   #pip install requests bs4 (install above libs)
# import json
import csv


def getStockData(stockSymbol):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36'}  #Good practice to customize header
    url = f'https://ca.finance.yahoo.com/quote/{stockSymbol}'

    ## Query website/server to get data back from webpage
    request = requests.get(url, headers = headers) 
    #TEST: print(request.status_code)   # print(request.text)  #print(request.json())


    ## Parse thru HTML document and find certain element contents
    soup = BeautifulSoup(request.text, 'html.parser')

    stock_info = { # Dictionary to store values
    'stockSymbol' : stockSymbol,
    'asset_name' : soup.title.text, #Search within soup --> Find 'title' tag --> get text
    'asset_price' : soup.find('div', {'class': 'D(ib) Mend(20px)'}).find_all('fin-streamer')[0].text,  #Finds specified TAG, its CLASS, and list of children within it in order 
    'asset_change' : soup.find('div', {'class': 'D(ib) Mend(20px)'}).find_all('fin-streamer')[1].text,
    'asset_change_percentage' : soup.find('div', {'class': 'D(ib) Mend(20px)'}).find_all('fin-streamer')[2].text
    # asset_price = soup.find('fin-streamer', {'class': 'Fw(b) Fz(36px) Mb(-4px) D(ib)'}).text   #Manual way to pinpoint element
    }

    ## Pretty Print Dict manually (Without imports)
    print('\n Creating file storing the following contents of SCRAPPED contents: \n')
    for key, value in stock_info.items():
        print(key, ' : ', value)
     
    ## Create file storing scrapped contents
    with open('CrawlScrap/data_collected_output/yahoo/ScrappedStockData.csv', 'w', encoding='UTF8') as file:  #w = write to file
        # json.dump(stock_info, file)  #If want to write to json file
        csvFile = csv.writer(file)
        csvFile.writerow(stock_info.items())

    return stock_info


#########################################################

## Examples to Test Functions
getStockData('TSLA')