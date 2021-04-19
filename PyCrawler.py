import gspread, os, openpyxl, subprocess
from datetime import date
from oauth2client.service_account import ServiceAccountCredentials

#variables globales:
stocks = ["AAPL", "ABEV", "ABT", "ADBE", "AGRO", "ADP", "AIG", "AMD", "AMGN", "AMX", "AMZN", "ARCO", "AUY", "AXP", "AZN", "BA", "BABA", "BBD", "BBDD", "BBVA", "BCS", "BHP", "BIDU", "BIIB", "BNG", "BP", "BRFS", "BSBR", "C", "CAT", "CHL", "CL", "COST", "CRM", "CSCO", "CVX", "CX", "DESP", "DISN", "DISND", "EBAY", "ERJ", "FB", "FDX", "FMX", "GE", "GGB", "GILD", "GILDD", "GLNT", "GLNTD", "GOLD", "GOLDD", "GOOGL", "GS", "GSK", "HD", "HMC", "HMY", "HPQ", "HSBC", "IBM", "INFY", "INTC", "ITUB", "JD", "JNJ", "JPM", "KO", "KOD", "LMT", "LVS", "LYG", "MCD", "MDT", "MELI", "MELID", "MMM", "MO", "MRK", "MSFT", "MSFTD", "NEM", "NFLX", "NKE", "NOKA", "NVDA", "NVS", "OGZD", "ORCL", "PBR", "PEP", "PFE", "PG", "PYPL", "QCOM", "RDS", "RIO", "RTX", "SAN", "SAP", "SBS", "SBUX", "SID", "SLB", "SNAP", "SNE", "T", "TEN", "TGT", "TM", "TOT", "TRIP", "TSLA", "TSLAD", "TSM", "TSU", "TWTR", "TXN", "TXR", "UGP", "UN", "V", "VALE", "VIST", "VIV", "VOD", "VRSN", "VZ", "WFC", "WMT", "WMTD", "X", "XOM", "XROX", "YELP"]
refused_list = []
invalid_list = []
pending_list = stocks.copy()

#Variables para el google spreadsheets:
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('secret.json',scope)
client = gspread.authorize(creds)

#chunk of code to create an Excel file
database = openpyxl.Workbook()
database.create_sheet(index = 0 , title = "CEDEARs")
cedears = database.active

def spreadsheets(task, col, row, data):
    rowcol=row+str(col+1)
    if task == 'put':
        print (rowcol, " = ", data)
        cedears[rowcol] = data
    elif task == 'get':
        return cedears[rowcol]
    else:
        print('tasks must be either "get" or "put"')
    database.save("C:\\Users\\Magnus\\VCS\\PyCrawler\\Stocks.xlsx")

#This function is deprecated: 
def google_spreadsheets(task, col, row, data):
    sheet = client.open("CEDEARs").get_worksheet(1)
    if task == 'put':
        sheet.update_cell(row, col, data)
    elif task == 'get':
        return sheet.cell(row, col)
    else:
        print('tasks must be either "get" or "put"')

def get_div(ticker):
    grabber = 'python historical_grabber.py ' + ticker + " div"
    try:
        div = subprocess.check_output(grabber)
        div = div.strip()
        return div
    except:
        return 0

def get_price(ticker):
    grabber = 'python historical_grabber.py ' + ticker + " price"
    try:
        price = subprocess.check_output(grabber)
        price = price.strip()
        return price
    except:
        return 1

def get_stats(ticker):
    grabber = 'python historical_grabber.py ' + ticker + " stats"
    try:
        price = subprocess.check_output(grabber)
        #price = price.strip()
        return price.decode().strip()
    except:
        return ("N/A")

#initialize spreadsheet
spreadsheets('put', 0, 'A', "Ticker")
spreadsheets('put', 0, 'B', "Price")
spreadsheets('put', 0, 'C', "Dividend")
spreadsheets('put', 0, 'D', "Yield")

spreadsheets('put', 0, 'F', "Market Cap (intraday)")
spreadsheets('put', 0, 'G', "Enterprise Value")
spreadsheets('put', 0, 'H', "Forward P/E")
spreadsheets('put', 0, 'I', "PEG Ratio (5 yr expected)")
spreadsheets('put', 0, 'J', "Price/Sales")
spreadsheets('put', 0, 'K', "Price/Book")
spreadsheets('put', 0, 'L', "Enterprise Value/Revenue")
spreadsheets('put', 0, 'M', "Enterprise Value/EBITDA")

spreadsheets('put', 0, 'O', "Updated on")

while (pending_list):
    for i in pending_list:
        d = float(get_div(i))
        p = float(get_price(i))
        s = get_stats(i)
        s = s.split("\n")
        y = round(d/p, 4)
        ix = stocks.index(i) +1

        spreadsheets('put', ix, 'A', i)
        spreadsheets('put', ix, 'B', p)
        spreadsheets('put', ix, 'C', d)
        spreadsheets('put', ix, 'D', y)



        cols = ['F','G','H','I','J','K','L','M']
        for c in cols:
            try:
                spreadsheets('put', ix, c, s[cols.index(c)].strip())
            except:
                spreadsheets('put', ix, c, "N/A")
        pending_list.remove(i)
        spreadsheets('put', ix, 'O', date.today())
