from datetime import datetime, timedelta
import time, requests, pandas, lxml, sys
from lxml import html
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def format_date(date_datetime):
    date_timetuple = date_datetime.timetuple()
    date_mktime = time.mktime(date_timetuple)
    date_int = int(date_mktime)
    date_str = str(date_int)
    return date_str

def subdomain(symbol, start, end, what):
    format_url = "{0}/history?period1={1}&period2={2}"
    if (what == "div"):
        tail_url = "&interval=div%7Csplit&filter=div&frequency=1d"
    else:
        if (what == "price"):
            tail_url = "&interval=div%7Csplit&filter=history&frequency=1d"
        else: 
            if (what == "stats"):
                tail_url = "/key-statistics?p="
                return (symbol + tail_url + symbol)
            else:
                print ("wrong \"what\".")
                exit(1)
    subdomain = format_url.format(symbol, start, end) + tail_url
    return subdomain

def header(subdomain):
    hdrs = {"authority": "finance.yahoo.com",
            "method": "GET",
            "path": subdomain,
            "scheme": "https",
            "accept": "text/html,application/xhtml+xml",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            "cookie": "cookies",
            "dnt": "1",
            "pragma": "no-cache",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0"}
    return hdrs

def scrape_page(url, header):
    #print ("scrape:", url)
    page = requests.get(url, headers=header)
    element_html = html.fromstring(page.content)
    table = element_html.xpath('//table')
    table_tree = lxml.etree.tostring(table[0], method='xml')
    panda = pandas.read_html(table_tree)
    return panda

if __name__ == '__main__':

    symbol = ''
    if len(sys.argv) == 0:
        print('please provide a ticker and a parameter')
    else:
        symbol = str(sys.argv[1])
        info = str(sys.argv[2])

    #create datetime objects
    start = datetime.today() - timedelta(days=9125)
    end = datetime.today()
    #properly format the date to epoch time
    start = format_date(start)
    end = format_date(end)
    what = info
    sub = subdomain(symbol, start, end, what)
    hdrs = header(sub)    
    base_url = "https://finance.yahoo.com/quote/"
    url = base_url + sub
    scrape = scrape_page(url, hdrs)

    pay = 0
    times = 0
    yiel = 0
    d = scrape[0]

    if (info == "div"):
        try:
            for i in range (1,10):
                e = d.iloc[i]
                divi = e.iloc[1].replace('Dividend', '').strip()
                date = e.iloc[0].split()
                year = date[2]
                if (year == "2020"):
                    pay += float(divi)
            print(pay)
        except:
            print('0')
        
    else:
        if (info == "price"):
            try:
                price = float(scrape[0].iloc[0].loc['Open'])
                print(price)
            except:
                print('1')
        else:
            if (info == "stats"): 
                try:
                    for i in range (0, 8): #Pensar cómo sacar los otros campos
                        print(scrape[0].iloc[i].iloc[1]) #son 8 en total. Iterar.
                except:
                    print ("error")
            else:
                print("must be either \"price\", \"stats\" or \"div\".")
                exit(1)
