# Liam Murphy
# quick and dirty script for stock data gathering

# imports
from td.client import TDClient

import json 
import time
import os

c_id_file = open("/Users/liammurphy/Documents/Personal/Projects/Python_Projects/trading/config/client_id")
client_id = c_id_file.read()
c_id_file.close()
ru_file = open("/Users/liammurphy/Documents/Personal/Projects/Python_Projects/trading/config/redirect_uri")
redirect_uri = ru_file.read()
ru_file.close()
acn_file = open("/Users/liammurphy/Documents/Personal/Projects/Python_Projects/trading/config/acc_num")
account_number = acn_file.read()
acn_file.close()
# begin script
session = TDClient(
    client_id=client_id,
    redirect_uri=redirect_uri
    account_number=account_number,
    credentials_path="/Users/liammurphy/Documents/Personal/Projects/Python_Projects/trading/config/td_state.json"
)

stock_list = ['A',
 'ABBV',
 'ABC',
 'ABT',
 'ACN',
 'ALB',
 'ALL',
 'AMT',
 'ANTM',
 'AON',
 'APD',
 'APTV',
 'AXP',
 'BA',
 'BABA',
 'BBY',
 'BDX',
 'BILL',
 'BRK.B',
 'BX',
 'BXP',
 'CAT',
 'CB',
 'CCI',
 'CI',
 'CLX',
 'CMI',
 'CNI',
 'COF',
 'CRM',
 'CTLT',
 'CVNA',
 'DASH',
 'DE',
 'DFS',
 'DG',
 'DGX',
 'DHR',
 'DIS',
 'DLR',
 'DRI',
 'DTE',
 'DUK',
 'ECL',
 'EL',
 'ETN',
 'ETR',
 'EW',
 'FDX',
 'FIS',
 'FVRR',
 'GD',
 'GME',
 'GPN',
 'GS',
 'HCA',
 'HD',
 'HLT',
 'IBM',
 'ICE',
 'IFF',
 'INFO',
 'ITW',
 'JNJ',
 'JPM',
 'KEYS',
 'KMB',
 'KMX',
 'KSU',
 'LHX',
 'LIN',
 'LLY',
 'LMT',
 'LOW',
 'MA',
 'MCD',
 'MCK',
 'MDT',
 'MMC',
 'MMM',
 'NET',
 'NKE',
 'NOW',
 'NSC',
 'PANW',
 'PG',
 'PLD',
 'PNC',
 'PPG',
 'PXD',
 'RL',
 'RSG',
 'SE',
 'SHOP',
 'SHW',
 'SNOW',
 'SPG',
 'SPGI',
 'SPOT',
 'SQ',
 'SRE',
 'STZ',
 'SWK',
 'SYK',
 'TDOC',
 'TEL',
 'TGT',
 'TMO',
 'TRU',
 'TRV',
 'TSM',
 'TT',
 'TWLO',
 'UNH',
 'UNP',
 'UPS',
 'V',
 'VMW',
 'W',
 'WM',
 'WMT',
 'WSM',
 'XPO',
 'YUM',
 'ZBH',
 'ZEN',
 'ZTS',
 'AAPL',
 'ABNB',
 'ACWI',
 'ADBE',
 'ADI',
 'ADP',
 'ADSK',
 'AKAM',
 'AMAT',
 'AMGN',
 'AMZN',
 'APPN',
 'AVGO',
 'BIDU',
 'BIIB',
 'BILI',
 'BNTX',
 'BYND',
 'CDNS',
 'CHKP',
 'CHTR',
 'CME',
 'COIN',
 'COST',
 'COUP',
 'CPRT',
 'CROX',
 'CRSP',
 'CRWD',
 'CTXS',
 'DDOG',
 'DOCU',
 'EA',
 'EMB',
 'ENPH',
 'ETSY',
 'EXAS',
 'EXPD',
 'EXPE',
 'FB',
 'FISV',
 'FTNT',
 'FUTU',
 'GOOG',
 'HON',
 'IBB',
 'IEF',
 'IEI',
 'ILMN',
 'INTU',
 'KLAC',
 'LRCX',
 'LULU',
 'MAR',
 'MBB',
 'MCHP',
 'MRNA',
 'MSFT',
 'MTCH',
 'NFLX',
 'NTES',
 'NTLA',
 'NVAX',
 'NVDA',
 'NXPI',
 'OKTA',
 'PAYX',
 'PDD',
 'PEP',
 'PTON',
 'PYPL',
 'QCOM',
 'QQQ',
 'QRVO',
 'ROKU',
 'ROST',
 'SBUX',
 'SEDG',
 'SHV',
 'SMH',
 'SPLK',
 'SWKS',
 'TEAM',
 'TER',
 'TLT',
 'TMUS',
 'TROW',
 'TSCO',
 'TSLA',
 'TTWO',
 'TXN',
 'UPST',
 'VRTX',
 'WDAY',
 'WYNN',
 'XLNX',
 'Z',
 'ZM',
 'ZS']
print(session.login())

for ticker in stock_list:
    time.sleep(0.51)
    filename = ticker + ".json"
    full_path = os.path.join("/Users/liammurphy/Documents/Personal/Projects/Python_Projects/trading/data/equities/", filename)
    new_json = open(full_path, "w")
    price_history_dict = session.get_price_history(symbol=ticker, period_type="year", period="20", frequency_type="daily", frequency="1")
    json.dump(price_history_dict, new_json)
