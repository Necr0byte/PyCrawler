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


def subdomain(symbol, start, end):
    format_url = "{0}/history?period1={1}&period2={2}"
    tail_url = "&interval=div%7Csplit&filter=div&frequency=1d"
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
    page = requests.get(url, headers=header)
    element_html = html.fromstring(page.content)
    table = element_html.xpath('//table')
    table_tree = lxml.etree.tostring(table[0], method='xml')
    panda = pandas.read_html(table_tree)
    return panda


def clean_dividends(symbol, dividends):
    index = len(dividends)
    dividends.name = symbol
    dividends = dividends.drop(index-1)
    dividends = dividends.set_index('Date')    
    dividends = dividends['Dividends']
    div_ret = dividends.str
    div_ret = div_ret.strip()
    # dividends = dividends.str.replace(r'\Dividend', '')
    # dividends = dividends.str.replace(r'\n','')
    # dividends = dividends.str.replace(r'\r','')
    # dividends = dividends.str.replace(r'b','')
    # dividends = dividends.str.replace(r'\b','')
    # dividends = dividends.str.replace(r'\'','')
    # dividends = dividends.str.replace(r' ','')
    # dividends = dividends.str.replace(r'Nos','')
    # dividends = dividends.str.strip()
    #re.sub("[^\d\.]", "", dividends)  # Acá hay que sacar todos los caracteres no-numéricos de dividends
    #dividends = dividends.astype(float)  # Sino la conversión a Float falla
    
    return div_ret


if __name__ == '__main__':

    symbol = ''

    if len(sys.argv) == 0:
        print('please provide a ticker')
    else:
        symbol = str(sys.argv[1])

    #create datetime objects
    start = datetime.today() - timedelta(days=9125)
    end = datetime.today()
    #properly format the date to epoch time
    start = format_date(start)
    end = format_date(end)
    #format the subdomain
    sub = subdomain(symbol, start, end)
    #customize the request header
    hdrs = header(sub)

    #concatenate the subdomain with the base URL
    base_url = "https://finance.yahoo.com/quote/"
    url = base_url + sub
    #scrape the dividend history table from Yahoo Finance
    dividends = scrape_page(url, hdrs)
    #clean the dividend history table
    clean_div = clean_dividends(symbol, dividends[0])

    try:
        #print("clean_div[-1]:")
        print(clean_div[-1])
    except:
        print('0')