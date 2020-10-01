"""Lists of Relevant Stocks"""
import pandas as pd

data_path = 'C:\\Users\\Jeff\\Documents\\Trading\\Python\\Data\\Alpha_vantage\\'

test_five = {'BAX', 'BBT', 'MGM', 'GPC', 'WYNN', 'VLO'}

test_port = {'INTU', 'NVR', 'CAT', 'BCI', 'DUK', 'WMT', 'JNJ'}

sp_500 = ['SPY', 'AAL', 'AAP', 'AAPL', 'ABBV', 'ABC', 'ABMD', 'ABT', 'ACN', 'ADBE', 'ADI',
          'ADM', 'ADP', 'ADS', 'ADSK', 'AEE', 'AEP', 'AES', 'AFL', 'AGN', 'AIG',
          'AIV', 'AIZ', 'AJG', 'AKAM', 'ALB', 'ALGN', 'ALK', 'ALL', 'ALLE', 'ALXN',
          'AMAT', 'AMD', 'AME', 'AMG', 'AMGN', 'AMP', 'AMT', 'AMZN', 'ANET', 'ANSS',
          'ANTM', 'AON', 'AOS', 'APA', 'APC', 'APD', 'APH', 'APTV', 'ARE', 'ARNC',
          'ATVI', 'AVB', 'AVGO', 'AVY', 'AWK', 'AXP', 'AZO', 'BA', 'BAC', 'BAX',
          'BBT', 'BBY', 'BDX', 'BEN', 'BHF', 'BHGE', 'BK', 'BKNG',
          'BLK', 'BLL', 'BMY', 'BR', 'BSX', 'BWA', 'BXP', 'C', 'CAG',
          'CAH', 'CAT', 'CB', 'CBOE', 'CBRE', 'CBS', 'CCI', 'CCL', 'CDNS', 'CE',
          'CELG', 'CERN', 'CF', 'CFG', 'CHD', 'CHRW', 'CHTR', 'CI', 'CINF', 'CL',
          'CLX', 'CMA', 'CMCSA', 'CME', 'CMG', 'CMI', 'CMS', 'CNC', 'CNP', 'COF',
          'COG', 'COO', 'COP', 'COST', 'COTY', 'CPB', 'CPRI', 'CPRT', 'CRM', 'CSCO',
          'CSX', 'CTAS', 'CTL', 'CTSH', 'CTXS', 'CVS', 'CVX', 'CXO', 'D', 'DAL',
          'DE', 'DFS', 'DG', 'DGX', 'DHI', 'DHR', 'DIS', 'DISCA', 'DISCK', 'DISH',
          'DLR', 'DLTR', 'DOV', 'DRE', 'DRI', 'DTE', 'DUK', 'DVA', 'DVN',
          'DXC', 'EA', 'EBAY', 'ECL', 'ED', 'EFX', 'EIX', 'EL', 'EMN', 'EMR',
          'EOG', 'EQIX', 'EQR', 'ES', 'ESS', 'ETFC', 'ETN', 'ETR', 'EVRG', 'EW',
          'EXC', 'EXPD', 'EXPE', 'EXR', 'F', 'FANG', 'FAST', 'FB', 'FBHS', 'FCX',
          'FDX', 'FE', 'FFIV', 'FIS', 'FISV', 'FITB', 'FL', 'FLIR', 'FLR', 'FLS',
          'FLT', 'FMC', 'FOX', 'FRC', 'FRT', 'FTI', 'FTNT', 'FTV', 'GD',
          'GE', 'GILD', 'GIS', 'GLW', 'GM', 'GOOG', 'GPC', 'GPN', 'GPS',
          'GRMN', 'GS', 'GT', 'GWW', 'HAL', 'HAS', 'HBAN', 'HBI', 'HCA', 'HCP',
          'HD', 'HES', 'HFC', 'HIG', 'HII', 'HLT', 'HOG', 'HOLX', 'HON', 'HP',
          'HPE', 'HPQ', 'HRB', 'HRL', 'HRS', 'HSIC', 'HST', 'HSY', 'HUM', 'IBM',
          'ICE', 'IDXX', 'IFF', 'ILMN', 'INCY', 'INFO', 'INTC', 'INTU', 'IP', 'IPG',
          'IPGP', 'IQV', 'IR', 'IRM', 'ISRG', 'IT', 'ITW', 'IVZ', 'JBHT', 'JCI',
          'J', 'JEF', 'JKHY', 'JNJ', 'JNPR', 'JPM', 'JWN', 'K', 'KEY', 'KEYS',
          'KHC', 'KIM', 'KLAC', 'KMB', 'KMI', 'KMX', 'KO', 'KR', 'KSS', 'KSU',
          'L', 'LB', 'LEG', 'LEN', 'LH', 'LIN', 'LKQ', 'LLY', 'LMT',
          'LNC', 'LNT', 'LOW', 'LRCX', 'LUV', 'LW', 'LYB', 'M', 'MA', 'MAA',
          'MAC', 'MAR', 'MAS', 'MAT', 'MCD', 'MCHP', 'MCK', 'MCO', 'MDLZ', 'MDT',
          'MET', 'MGM', 'MHK', 'MKC', 'MLM', 'MMC', 'MMM', 'MNST', 'MO', 'MOS',
          'MPC', 'MRK', 'MRO', 'MS', 'MSCI', 'MSFT', 'MSI', 'MTB', 'MTD', 'MU',
          'MXIM', 'MYL', 'NBL', 'NCLH', 'NDAQ', 'NEE', 'NEM', 'NFLX', 'NI',
          'NKE', 'NKTR', 'NLSN', 'NOC', 'NOV', 'NRG', 'NSC', 'NTAP', 'NTRS', 'NUE',
          'NVDA', 'NWL', 'NWS', 'NWSA', 'O', 'OKE', 'OMC', 'ORCL', 'ORLY', 'OXY',
          'PAYX', 'PBCT', 'PCAR', 'PEG', 'PEP', 'PFE', 'PFG', 'PG', 'PGR', 'PH',
          'PHM', 'PKG', 'PKI', 'PLD', 'PM', 'PNC', 'PNR', 'PNW', 'PPG', 'PPL',
          'PRGO', 'PRU', 'PSA', 'PSX', 'PVH', 'PWR', 'PXD', 'PYPL', 'QCOM', 'QRVO',
          'RCL', 'RE', 'REG', 'REGN', 'RF', 'RHI', 'RHT', 'RJF', 'RL', 'RMD',
          'ROK', 'ROL', 'ROP', 'ROST', 'RSG', 'RTN', 'SBAC', 'SBUX', 'SCHW', 'SEE',
          'SHW', 'SIVB', 'SJM', 'SLB', 'SLG', 'SNA', 'SNPS', 'SO', 'SPG', 'SPGI',
          'SRE', 'STI', 'STT', 'STX', 'STZ', 'SWK', 'SWKS', 'SYF', 'SYK', 'SYMC',
          'SYY', 'T', 'TAP', 'TDG', 'TEL', 'TFX', 'TGT', 'TIF', 'TJX', 'TMK',
          'TMO', 'TPR', 'TRIP', 'TROW', 'TRV', 'TSCO', 'TSN', 'TSS', 'TTWO', 'TWTR',
          'TXN', 'TXT', 'UA', 'UAA', 'UAL', 'UDR', 'UHS', 'ULTA', 'UNH', 'UNM',
          'UNP', 'UPS', 'URI', 'USB', 'UTX', 'V', 'VAR', 'VFC', 'VIAB', 'VLO',
          'VMC', 'VNO', 'VRSK', 'VRSN', 'VRTX', 'VTR', 'VZ', 'WAT', 'WBA', 'WCG',
          'WDC', 'WEC', 'WELL', 'WFC', 'WHR', 'WLTW', 'WM', 'WMB', 'WMT', 'WRK',
          'WU', 'WY', 'WYNN', 'XEC', 'XEL', 'XLNX', 'XOM', 'XRAY', 'XRX', 'XYL',
          'YUM', 'ZBH', 'ZION', 'ZTS','AMD','TSS','SYMC','TMK','APC','HRS',
          'RHT','VIX', 'A', 'AMCR', 'ATO', 'BHGE', 'BY', 'CELG', 'CTVA', 'GL',
          'IEX', 'SYMC', 'LDOS', 'LHX', 'MKTX', 'TMUS','WAB', 'FNG','TSLA', 'SPY','QQQ']

###SP500:^GSPC, DJI:^DJI, NYSE:^NYA, Russell:^RUT, NASDAQ:^IXIC, Nikkei:^N225
indices = ['GSPC', 'DJI', 'NYA', 'RUT', 'IXIC', 'N225', 'NYSE','NASDAQ','SPY','QQQ']

nasdaq = 'NASDAQ'
df = pd.read_csv(data_path + nasdaq + '\\' + nasdaq + '.csv')
nasdaq = [stk for stk in df.iloc[:,0]]


direxion_3x = ['SPXL','SPXS','SPY']

sp_600 = 'sp_600'
df = pd.read_csv('C:\\Users\\Jeff\\Documents\\Trading\\Python\\Data\\NLP\\'+sp_600+'.csv')
sp_600 = [stk for stk in df.iloc[:,0]]


fiveyd = pd.read_csv('C:\\Users\\Jeff\\Documents\\Trading\\Python\\Data\\NLP\\five_years_dollars.csv')
fiveyd = [stk for stk in fiveyd.iloc[:,0]]











