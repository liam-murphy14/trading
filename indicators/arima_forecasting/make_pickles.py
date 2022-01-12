# Liam Murphy
"""a little file to make and store the pickles when i want to update the models because without this it would take like 5 hours every time i want to update"""

from forecast_testing import create_auto_arima, json_to_dataframe, StoredArima
import pickle
import os 
from td.client import TDClient
import time
import pandas as pd
import datetime

c_id_file = open("/Users/liammurphy/Documents/Personal/Projects/Python_Projects/trading/config/client_id")
client_id = c_id_file.read()
c_id_file.close()
ru_file = open("/Users/liammurphy/Documents/Personal/Projects/Python_Projects/trading/config/redirect_uri")
redirect_uri = ru_file.read()
ru_file.close()
acn_file = open("/Users/liammurphy/Documents/Personal/Projects/Python_Projects/trading/config/acc_num")
account_number = acn_file.read()
acn_file.close()
session = TDClient(
    client_id=client_id,
    redirect_uri=redirect_uri
    account_number=account_number,
    credentials_path="/Users/liammurphy/Documents/Personal/Projects/Python_Projects/trading/config/td_state.json"
)

ticker_list = ['A',
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

def make_fresh_pickles():
    os.system("python3 data_to_json.py")
    for ticker in ticker_list:
        ticker_data = json_to_dataframe(ticker)
        all_closes = ticker_data["close"]
        new_fitted = create_auto_arima(all_closes)
        newest_datetime = ticker_data.index[-1]
        to_store = StoredArima(new_fitted, newest_datetime)
        name = ticker + ".pickle"
        full_path = os.path.join("/Users/liammurphy/Documents/Personal/Projects/Python_Projects/trading/indicators/arima_forecasting/arima_pickles/", name)
        file = open(full_path, "wb")
        pickle.dump(to_store, file)
        file.close()

    for ticker in ticker_list:
        time.sleep(0.501)
        d = session.get_price_history(symbol=ticker, period_type="month", period="1", frequency_type="daily", frequency="1")
        candles = pd.DataFrame(d["candles"])
        actual_dts = [datetime.datetime.fromtimestamp(mils / 1000) for mils in candles["datetime"]]
        candles["datetime"] = actual_dts
        candles.set_index("datetime", inplace=True)
        name = ticker + ".pickle"
        full_path = os.path.join("/Users/liammurphy/Documents/Personal/Projects/Python_Projects/trading/indicators/arima_forecasting/arima_pickles/", name)
        file = open(full_path, "rb")
        old_arima = pickle.load(file)
        file.close()
        fitted = old_arima.fitted
        new_dt = old_arima.newest_datetime
        new_rows = candles[lambda x : x.index > new_dt]
        if new_rows.empty:
            print("no new data for " + ticker)
            continue
        fitted.update(new_rows["close"])
        updated_new_dt = candles.index[-1]
        new_to_save = StoredArima(fitted, updated_new_dt)
        file = open(full_path, "wb")
        pickle.dump(new_to_save, file)
        file.close()

choice = input("what kind of pickles would you like ??\noptions: [u]pdated or [f]resh\n")
if choice == "f":
    make_fresh_pickles()
elif choice == "u":
    update_existing_pickles()
else:
    print("choose a valid letter")
