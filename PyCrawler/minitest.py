import httplib2

url = 'https://www.marketbeat.com/stocks/NASDAQ/AAPL/dividend/'
success = 'Yield:</strong></td><td>'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'
            ,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
            ,
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.google.com/',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        }

(resp, contents) = httplib2.Http().request(url, headers=headers)
deco_contents = str(contents, 'utf-8', errors='ignore')
if deco_contents.find(success) != -1 :
    div_yield = deco_contents[deco_contents.find(success)+len(success):deco_contents.find(success)+len(success)+4]
    print(div_yield)
#print(deco_contents)
print(resp)


