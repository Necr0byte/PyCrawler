import httplib2
#import re
import random
#from collections import OrderedDict
import gspread
from oauth2client.service_account import ServiceAccountCredentials

#variables globales:
stocks = ["AAPL", "ABEV", "ABT", "ADBE", "AGRO", "ADP", "AIG", "AMD", "AMGN", "AMX", "AMZN", "ARCO", "AUY", "AXP", "AZN", "BA", "BABA", "BBD", "BBDD", "BBVA", "BCS", "BHP", "BIDU", "BIIB", "BNG", "BP", "BRFS", "BSBR", "C", "CAT"] #, "CHL", "CL", "COST", "CRM", "CSCO", "CVX", "CX", "DESP", "DISN", "DISND", "EBAY", "ERJ", "FB", "FDX", "FMX", "GE", "GGB", "GILD", "GILDD", "GLNT", "GLNTD", "GOLD", "GOLDD", "GOOGL", "GS", "GSK", "HD", "HMC", "HMY", "HPQ", "HSBC", "IBM", "INFY", "INTC", "ITUB", "JD", "JNJ", "JPM", "KO", "KOD", "LMT", "LVS", "LYG", "MCD", "MDT", "MELI", "MELID", "MMM", "MO", "MRK", "MSFT", "MSFTD", "NEM", "NFLX", "NKE", "NOKA", "NVDA", "NVS", "OGZD", "ORCL", "PBR", "PEP", "PFE", "PG", "PYPL", "QCOM", "RDS", "RIO", "RTX", "SAN", "SAP", "SBS", "SBUX", "SID", "SLB", "SNAP", "SNE", "T", "TEN", "TGT", "TM", "TOT", "TRIP", "TSLA", "TSLAD", "TSM", "TSU", "TWTR", "TXN", "TXR", "UGP", "UN", "V", "VALE", "VIST", "VIV", "VOD", "VRSN", "VZ", "WFC", "WMT", "WMTD", "X", "XOM", "XROX", "YELP"]
refused_list = []
invalid_list = []
pending_list = stocks.copy()

resp = ''
contents = ''

retry = 3
r = 0

#Webs a scrapear. Por ahora, una.
base_url = ['https://seekingalpha.com/symbol/', 'https://stocknews.com/stock/']
trailing_url = ['/dividends/yield', '/dividends/']
trailing_url_no_div = '/dividends/no-dividends'


#Variables para el google spreadsheets:
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('secret.json',scope)
client = gspread.authorize(creds)

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
                print(div_yield)
                index = stocks.index(i)
                spreadsheets('replace',1,index+1,i)
                spreadsheets('replace',2,index+1,div_yield)
                pending_list.remove(i)
            else:
                print('kicked me out!')
                refused_list.append(i)
        else:
            #Check no-dividend url
            url = prefix + ticker + suffix_nodiv
            (resp, contents) = httplib2.Http().request(url, headers=headers)
            deco_contents = str(contents, 'utf-8', errors='ignore')
            if resp.status == 200:
                if deco_contents.find(fail) != -1 :
                    print('has no dividend')
                    index = stocks.index(i)
                    spreadsheets('replace',1,index+1,i)
                    spreadsheets('replace',2,index+1,0)
                    pending_list.remove(i)
                else:
                    print('I found no-div url, but not the text!')
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
            index = stocks.index(i)
            spreadsheets('replace',1,index+1,i)
            spreadsheets('replace',2,index+1,'ERROR')
            invalid_list.append(i)
            pending_list.remove(i)

def spreadsheets(task, col, row, data):

    sheet = client.open("CEDEARs").get_worksheet(1)
    if task == 'insert':
        sheet.insert_row(data,row)
    elif task == 'replace':
        sheet.update_cell(row, col, data)
    elif task == 'query':
        return sheet.cell(row,col)
    elif task == 'find' :
        print("hace la búsqueda, cabezón!")  #devolver columna, fila de un texto - Vale la pena? No es muy lento?
    elif task == 'delete':
        sheet.update_cell(row,col,'')
    else: print('task must be "insert", "replace", "query, "find" or "delete" ')


for i in stocks:
    spreadsheets('replace', 1, stocks.index(i)+1, i)

while (pending_list):
    print('pending list is: ', f'{pending_list}')
    print('Trying SeekingAlpha')
    for i in pending_list:
        busca_div(base_url[0], i,trailing_url[0], trailing_url_no_div, '"div_yield_fwd":', 'No dividends for')
    print('pending list is: ', f'{pending_list}')
    print('Trying StockNews')
    for i in pending_list:
        busca_div(base_url[1], i,trailing_url[1], trailing_url[1], 'Dividend yield</td><td class=text-right>', 'N/A</td')
