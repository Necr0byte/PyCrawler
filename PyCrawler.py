import gspread, os, openpyxl, subprocess
from datetime import date
from oauth2client.service_account import ServiceAccountCredentials

#variables globales:
cedear_list = ["AAPL", "ABEV", "ABT", "ADBE", "AGRO", "ADP", "AIG", "AMD", "AMGN", "AMX", "AMZN", "ARCO", "AUY", "AXP", "AZN", "BA", "BABA", "BBD", "BBDD", "BBVA", "BCS", "BHP", "BIDU", "BIIB", "BNG", "BP", "BRFS", "BSBR", "C", "CAT", "CHL", "CL", "COST", "CRM", "CSCO", "CVX", "CX", "DESP", "DISN", "DISND", "EBAY", "ERJ", "FB", "FDX", "FMX", "GE", "GGB", "GILD", "GILDD", "GLOB", "GLNTD", "GOLD", "GOLDD", "GOOGL", "GS", "GSK", "HD", "HMC", "HMY", "HPQ", "HSBC", "IBM", "INFY", "INTC", "ITUB", "JD", "JNJ", "JPM", "KO", "KOD", "LMT", "LVS", "LYG", "MCD", "MDT", "MELI", "MELID", "MMM", "MO", "MRK", "MSFT", "MSFTD", "NEM", "NFLX", "NKE", "NOKA", "NVDA", "NVS", "OGZD", "ORCL", "PBR", "PEP", "PFE", "PG", "PYPL", "QCOM", "RDS", "RIO", "RTX", "SAN", "SAP", "SBS", "SBUX", "SID", "SLB", "SNAP", "SNE", "T", "TEN", "TGT", "TM", "TOT", "TRIP", "TSLA", "TSLAD", "TSM", "TSU", "TWTR", "TXN", "TXR", "UGP", "UN", "V", "VALE", "VIST", "VIV", "VOD", "VRSN", "VZ", "WFC", "WMT", "WMTD", "X", "XOM", "XROX", "YELP"]
sp500_list = ['A','AAL','AAP','AAPL','ABBV','ABC','ABMD','ABT','ACN','ADBE','ADI','ADM','ADP','ADSK','AEE','AEP','AES','AFL','AIG','AIZ','AJG','AKAM','ALB','ALGN','ALK','ALL','ALLE','ALXN','AMAT','AMCR','AMD','AME','AMGN','AMP','AMT','AMZN','ANET','ANSS','ANTM','AON','AOS','APA','APD','APH','APTV','ARE','ATO','ATVI','AVB','AVGO','AVY','AWK','AXP','AZO','BA','BAC','BAX','BBY','BDX','BEN','BF.B','BIIB','BIO','BK','BKNG','BKR','BLK','BLL','BMY','BR','BRK.B','BSX','BWA','BXP','C','CAG','CAH','CARR','CAT','CB','CBOE','CBRE','CCI','CCL','CDNS','CDW','CE','CERN','CF','CFG','CHD','CHRW','CHTR','CI','CINF','CL','CLX','CMA','CMCSA','CME','CMG','CMI','CMS','CNC','CNP','COF','COG','COO','COP','COST','CPB','CPRT','CRM','CSCO','CSX','CTAS','CTLT','CTSH','CTVA','CTXS','CVS','CVX','CZR','D','DAL','DD','DE','DFS','DG','DGX','DHI','DHR','DIS','DISCA','DISCK','DISH','DLR','DLTR','DOV','DOW','DPZ','DRE','DRI','DTE','DUK','DVA','DVN','DXC','DXCM','EA','EBAY','ECL','ED','EFX','EIX','EL','EMN','EMR','ENPH','EOG','EQIX','EQR','ES','ESS','ETN','ETR','ETSY','EVRG','EW','EXC','EXPD','EXPE','EXR','F','FANG','FAST','FB','FBHS','FCX','FDX','FE','FFIV','FIS','FISV','FITB','FLIR','FLT','FMC','FOX','FOXA','FRC','FRT','FTNT','FTV','GD','GE','GILD','GIS','GL','GLW','GM','GNRC','GOOG','GOOGL','GPC','GPN','GPS','GRMN','GS','GWW','HAL','HAS','HBAN','HBI','HCA','HD','HES','HFC','HIG','HII','HLT','HOLX','HON','HPE','HPQ','HRL','HSIC','HST','HSY','HUM','HWM','IBM','ICE','IDXX','IEX','IFF','ILMN','INCY','INFO','INTC','INTU','IP','IPG','IPGP','IQV','IR','IRM','ISRG','IT','ITW','IVZ','J','JBHT','JCI','JKHY','JNJ','JNPR','JPM','K','KEY','KEYS','KHC','KIM','KLAC','KMB','KMI','KMX','KO','KR','KSU','L','LB','LDOS','LEG','LEN','LH','LHX','LIN','LKQ','LLY','LMT','LNC','LNT','LOW','LRCX','LUMN','LUV','LVS','LW','LYB','LYV','MA','MAA','MAR','MAS','MCD','MCHP','MCK','MCO','MDLZ','MDT','MET','MGM','MHK','MKC','MKTX','MLM','MMC','MMM','MNST','MO','MOS','MPC','MPWR','MRK','MRO','MS','MSCI','MSFT','MSI','MTB','MTD','MU','MXIM','NCLH','NDAQ','NEE','NEM','NFLX','NI','NKE','NLOK','NLSN','NOC','NOV','NOW','NRG','NSC','NTAP','NTRS','NUE','NVDA','NVR','NWL','NWS','NWSA','NXPI','O','ODFL','OKE','OMC','ORCL','ORLY','OTIS','OXY','PAYC','PAYX','PBCT','PCAR','PEAK','PEG','PENN','PEP','PFE','PFG','PG','PGR','PH','PHM','PKG','PKI','PLD','PM','PNC','PNR','PNW','POOL','PPG','PPL','PRGO','PRU','PSA','PSX','PVH','PWR','PXD','PYPL','QCOM','QRVO','RCL','RE','REG','REGN','RF','RHI','RJF','RL','RMD','ROK','ROL','ROP','ROST','RSG','RTX','SBAC','SBUX','SCHW','SEE','SHW','SIVB','SJM','SLB','SNA','SNPS','SO','SPG','SPGI','SRE','STE','STT','STX','STZ','SWK','SWKS','SYF','SYK','SYY','T','TAP','TDG','TDY','TEL','TER','TFC','TFX','TGT','TJX','TMO','TMUS','TPR','TRMB','TROW','TRV','TSCO','TSLA','TSN','TT','TTWO','TWTR','TXN','TXT','TYL','UA','UAA','UAL','UDR','UHS','ULTA','UNH','UNM','UNP','UPS','URI','USB','V','VAR','VFC','VIAC','VLO','VMC','VNO','VRSK','VRSN','VRTX','VTR','VTRS','VZ','WAB','WAT','WBA','WDC','WEC','WELL','WFC','WHR','WLTW','WM','WMB','WMT','WRB','WRK','WST','WU','WY','WYNN','XEL','XLNX','XOM','XRAY','XYL','YUM','ZBH','ZBRA','ZION','ZTS']
#stocks = cedear_list.copy()
stocks = sp500_list.copy()
refused_list = []
invalid_list = []
pending_list = stocks.copy()

#Variables para el google spreadsheets:
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('secret.json',scope)
client = gspread.authorize(creds)

#chunk of code to create an Excel file
database = openpyxl.Workbook()
database.create_sheet(index = 0 , title = "CEDEARs") #Crear sólo si no existe
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
    #database.save(".\\Stocks.xlsx")
    database.save(".\\Stocks-SP500.xlsx")

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
        return price.decode().strip()
    except:
        return ("N/A")

#initialize spreadsheet
try:
    spreadsheets('put', 0, 'A', "Ticker")
    spreadsheets('put', 0, 'B', "Price")
    spreadsheets('put', 0, 'C', "Dividend")
    spreadsheets('put', 0, 'D', "Yield")
    spreadsheets('put', 0, 'E', "Market Cap (intraday)")
    spreadsheets('put', 0, 'F', "Enterprise Value")
    spreadsheets('put', 0, 'G', "Trailing P/E")
    spreadsheets('put', 0, 'H', "Trailing P/E")
    spreadsheets('put', 0, 'H', "Forward P/E")
    spreadsheets('put', 0, 'I', "PEG Ratio (5 yr expected)")
    spreadsheets('put', 0, 'J', "Price/Sales ttm")
    spreadsheets('put', 0, 'K', "Price/Book mrq")
    spreadsheets('put', 0, 'L', "Enterprise Value/Revenue")
    spreadsheets('put', 0, 'M', "Enterprise Value/EBITDA")
    spreadsheets('put', 0, 'N', "Beta (5Y My.)")
    spreadsheets('put', 0, 'O', "52-Week Change")
    spreadsheets('put', 0, 'P', "S&P500 52-Week Change")
    spreadsheets('put', 0, 'Q', "52 Week High")
    spreadsheets('put', 0, 'R', "52 Week Low")
    spreadsheets('put', 0, 'S', "50-Day MA")
    spreadsheets('put', 0, 'T', "200-Day MA")
    spreadsheets('put', 0, 'U', "Avg Vol (3 mo.)")
    spreadsheets('put', 0, 'V', "Avg Vol (10 d.)")
    spreadsheets('put', 0, 'W', "Shares Outstanding")
    spreadsheets('put', 0, 'X', "Implied Shares Outstanding")
    spreadsheets('put', 0, 'Y', "Float")
    spreadsheets('put', 0, 'Z', "% Held by Insiders")
    spreadsheets('put', 0, 'AA', "% Held by Institutions")
    spreadsheets('put', 0, 'AB', "Shares Short")
    spreadsheets('put', 0, 'AC', "Short Ratio")
    spreadsheets('put', 0, 'AD', "Short % of Float")
    spreadsheets('put', 0, 'AE', "Short % of Shares Outst.")
    spreadsheets('put', 0, 'AF', "Shares Short (prev. mo.)")
    spreadsheets('put', 0, 'AG', "Forward Dividend")
    spreadsheets('put', 0, 'AH', "Forward Div. Yield")
    spreadsheets('put', 0, 'AI', "Trailing Dividend")
    spreadsheets('put', 0, 'AJ', "Trailing Div. Yield")
    spreadsheets('put', 0, 'AK', "5 Y. Avg. Div. Yield")
    spreadsheets('put', 0, 'AL', "P/O Ratio")
    spreadsheets('put', 0, 'AM', "Dividend Date")
    spreadsheets('put', 0, 'AN', "Ex-Dividend Date")
    spreadsheets('put', 0, 'AO', "Last Split Factor")
    spreadsheets('put', 0, 'AP', "Last Split Date")
    spreadsheets('put', 0, 'AQ', "Fiscal Year Ends")
    spreadsheets('put', 0, 'AR', "MRQ")
    spreadsheets('put', 0, 'AS', "Profit Margin")
    spreadsheets('put', 0, 'AT', "Operating Margin (ttm)")
    spreadsheets('put', 0, 'AU', "Return on Assets")
    spreadsheets('put', 0, 'AV', "Return on Equity")
    spreadsheets('put', 0, 'AW', "Revenue (ttm)")
    spreadsheets('put', 0, 'AX', "Revenue Per Share (ttm)")
    spreadsheets('put', 0, 'AY', "Q. Revenue Growth (yoy)")
    spreadsheets('put', 0, 'AZ', "Gross Profit (ttm)")
    spreadsheets('put', 0, 'BA', "EBITDA")
    spreadsheets('put', 0, 'BB', "Net Income Avi to Common (ttm)")
    spreadsheets('put', 0, 'BC', "Diluted EPS (ttm)")
    spreadsheets('put', 0, 'BD', "Q. Earnings Growth (yoy)")

    spreadsheets('put', 0, 'BF', "Updated on")
except: 
    print("couldn't write to spreadsheet")
    exit


while (pending_list):
    for i in pending_list:
        d = float(get_div(i))
        p = float(get_price(i))
        s = get_stats(i)
        s = s.split("\n")
        y = round(d/p, 4)
        ix = stocks.index(i) +1
        updated_on = spreadsheets('get', ix, 'BF', 1)

        if (updated_on != date.today()):
            spreadsheets('put', ix, 'A', i)
            spreadsheets('put', ix, 'B', p)
            spreadsheets('put', ix, 'C', d)
            spreadsheets('put', ix, 'D', y)

            cols = ['E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','AA','AB','AC','AD','AE','AF','AG','AH','AI','AJ','AK','AL','AM','AN','AO','AP','AQ','AR','AS','AT','AU','AV','AW','AX','AY','AZ','BA','BB','BC','BD']
            for c in cols:
                try:
                    spreadsheets('put', ix, c, s[cols.index(c)].strip())
                except:
                    spreadsheets('put', ix, c, "N/A")
            pending_list.remove(i)
            spreadsheets('put', ix, 'BF', date.today())

