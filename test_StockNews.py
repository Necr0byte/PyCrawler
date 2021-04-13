import httplib2
import re
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials

#variables globales:
stocks = ["AAPL", "ABEV", "ABT", "ADBE", "AGRO", "ADP", "AIG", "AMD", "AMGN", "AMX", "AMZN", "ARCO", "AUY", "AXP", "AZN", "BA", "BABA", "BBD", "BBDD", "BBVA", "BCS", "BHP", "BIDU", "BIIB", "BNG", "BP", "BRFS", "BSBR", "C", "CAT"] #, "CHL", "CL", "COST", "CRM", "CSCO", "CVX", "CX", "DESP", "DISN", "DISND", "EBAY", "ERJ", "FB", "FDX", "FMX", "GE", "GGB", "GILD", "GILDD", "GLNT", "GLNTD", "GOLD", "GOLDD", "GOOGL", "GS", "GSK", "HD", "HMC", "HMY", "HPQ", "HSBC", "IBM", "INFY", "INTC", "ITUB", "JD", "JNJ", "JPM", "KO", "KOD", "LMT", "LVS", "LYG", "MCD", "MDT", "MELI", "MELID", "MMM", "MO", "MRK", "MSFT", "MSFTD", "NEM", "NFLX", "NKE", "NOKA", "NVDA", "NVS", "OGZD", "ORCL", "PBR", "PEP", "PFE", "PG", "PYPL", "QCOM", "RDS", "RIO", "RTX", "SAN", "SAP", "SBS", "SBUX", "SID", "SLB", "SNAP", "SNE", "T", "TEN", "TGT", "TM", "TOT", "TRIP", "TSLA", "TSLAD", "TSM", "TSU", "TWTR", "TXN", "TXR", "UGP", "UN", "V", "VALE", "VIST", "VIV", "VOD", "VRSN", "VZ", "WFC", "WMT", "WMTD", "X", "XOM", "XROX", "YELP"]
refused_list = []
invalid_list = []
pending_list = stocks

resp = ''
contents = ''

retry = 3
r = 0

#Webs a scrapear. Por ahora, una. 
base_url = ['https://seekingalpha.com/symbol/', 'https://stocknews.com/stock/', 'https://www.marketbeat.com/stocks/NASDAQ/']
trailing_url = ['/dividends/yield', '/dividends/', '/dividend/']
trailing_url_no_div = '/dividends/no-dividends'


def randomize_headers():
    headers_list = [
    {  # Firefox 77 Mac
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0'
            ,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
            ,
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.google.com/',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        }, {  # Firefox 77 Windows
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'
            ,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
            ,
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.google.com/',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        }, {  # Chrome 83 Mac
        'Connection': 'keep-alive',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
            ,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
            ,
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://www.google.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }, {  # Chrome 83 Windows
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
            ,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
            ,
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://www.google.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        }]

    for i in range(1, 4):
        headers = random.choice(headers_list)
    return headers
	

def busca_div(prefix, ticker, suffix, suffix_nodiv, success, fail):
    url = prefix + ticker + suffix
    headers = randomize_headers()
    (resp, contents) = httplib2.Http().request(url, headers=headers)
    div_yield = ''
    if resp.status == 200:
        deco_contents = str(contents, 'utf-8', errors='ignore')
        print(i)
        if deco_contents.find(success) != -1 :
           div_yield = deco_contents[deco_contents.find(success)+len(success):deco_contents.find(success)+len(success)+4]
           if div_yield != 'null':               
               #grabar rendimiento en el excel
               index = stocks.index(i)
               pending_list.remove(i)
               print(i, div_yield)
           else:   
               print('kicked me out!')
               refused_list.append(i)
        else:
            #Check no-dividend url
            url = prefix + ticker + suffix_nodiv
            (resp, contents) = httplib2.Http().request(url, headers=headers)
            deco_contents = str(contents, 'utf-8', errors='ignore')
            if resp.status == 200:
                if deco_contents.find(success) != -1 :
                    index = stocks.index(i)
                    print('0', i)                    
                    pending_list.remove(i)
                else:
                    print('I found no-div url, but not the text!')
                    print(url)
                    print(fail)
            else:
                print('I didn\'t find the no-div url!')
                print(resp.status) 
                print(url)
    else:
        if resp.status == 403:
            print('Connection refused')
            refused_list.append(i)
            #Agregar a refused_list
        else:    
            print(i, ' is not found here')
            print(url)
            print(resp)
            index = stocks.index(i)
            invalid_list.append(i)
            pending_list.remove(i)
			
			
for i in stocks:
    print (i, stocks.index(i)+1)

while (pending_list):
    print('pending list is: ', f'{pending_list}')
    print('Trying marketbeat')
    for i in pending_list:
        busca_div(base_url[2], i,trailing_url[2], '', 'Yield:</strong></td><td>', 'Dividend Yield<strong>N/A<')