# Liam Murphy
"""
A module to open my trades. Records taken trades in that week's trade report.
gets all newest quotes
unpickles and updates models then gets predictions and stores them in a big ol dataframe (maybe using a user defined class or just tuples)
try to grab all options quotes at the same time
HERES WHERE WE GOTTA BE QUICK
find closest options spread to prediction and find bid ask and find trades in order of rr all VERY fast ideally with dataframes
"""

from td.client import TDClient, OptionChain
from forecast_testing import StoredArima
import pickle
import datetime
import os
import time
import pandas as pd

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


# global variables
expo_date = input("expiration date (format: yyyy-mm-dd): ")
days_to_expo = input("days to expiration: ")
trading_days = int(days_to_expo) - int(input("weekend days: "))
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
quote_df = pd.DataFrame(session.get_quotes(ticker_list))
forecast_dict = dict()

def unpickle(ticker : str):
    full_path = os.path.join("/Users/liammurphy/Documents/Personal/Projects/Python_Projects/trading/indicators/arima_forecasting/arima_pickles/", ticker + ".pickle")
    file = open(full_path, "rb")
    stored_arima = pickle.load(file)
    file.close()
    return stored_arima.fitted

def format_quote(ticker : str):
    close = quote_df[ticker]["closePrice"]
    current_dt = datetime.datetime.now()
    dic = {current_dt : close}
    return pd.Series(dic)

# update models with quotes and forecast price
for ticker in ticker_list:
    fitted = unpickle(ticker)
    # CHECK THIS EVERY TIME
    # comment out next line if testing on weekend
    fitted.update(format_quote(ticker))
    fc, ci = fitted.predict(n_periods=trading_days, return_conf_int=True)
    close = fc[trading_days - 1]
    low = ci[trading_days - 1, 0]
    high = ci[trading_days - 1, 1]
    forecast_dict[ticker] = [int(low), round(close), int(high) + 1]

# trading log and forecast df instead of dict
forecast_df = pd.DataFrame(forecast_dict, index=["low", "forecast", "high"])
t_log_path = os.path.join("/Users/liammurphy/Documents/Personal/Projects/Python_Projects/trading/systems/weekly_price_forecasting/trading_logs/", expo_date + "_log.csv")
trading_log = open(t_log_path, "w")
trading_log.write("ticker,spread,opening credit,max risk,reward/risk,comment\n")

# heres the opening trades part, gotta be mad quick
for ticker in ticker_list:
    time.sleep(0.5)
    strikes_too_wide = False
    tick_ops = OptionChain(ticker, strike_count=40, from_date=expo_date, to_date=expo_date)
    chain_key = expo_date + ':' + days_to_expo
    low = float(forecast_df[ticker]["low"])
    high = float(forecast_df[ticker]["high"])
    # BEGIN FAST CODE 
    ops_chain = session.get_options_chain(tick_ops)
    if ops_chain["status"] == "FAILED":
        trading_log.write(f"{ticker},N/A,N/A,N/A,N/A,no options for this expo date\n")
        continue
    call_chain = ops_chain["callExpDateMap"][chain_key]
    put_chain = ops_chain["putExpDateMap"][chain_key]
    strike_list = [float(strike) for strike in call_chain.keys()]
    strike_list.sort()
    if low <= min(strike_list) or high >= max(strike_list):
        # TESTING ONLY
        strikes_too_wide = True 
    else:
        while low not in strike_list:
            low = round(low - 0.5, 1)
            if low <= min(strike_list) or high >= max(strike_list):
                # TESTING ONLY
                strikes_too_wide = True
                break
        while high not in strike_list:
            high = round(high + 0.5, 1)
            if low <= min(strike_list) or high >= max(strike_list):
                # TESTING ONLY
                strikes_too_wide = True 
                break
        if low == min(strike_list) or high == max(strike_list) or strikes_too_wide:
            # TESTING ONLY
            trading_log.write(f"{ticker},N/A,N/A,N/A,N/A,strikes too wide\n")
            continue
        call_to_sell = call_chain[str(high)][0]
        long_call_strike = strike_list[strike_list.index(high) + 1]
        call_to_buy = call_chain[str(long_call_strike)][0]
        put_to_sell = put_chain[str(low)][0]
        long_put_strike = strike_list[strike_list.index(low) - 1]
        put_to_buy = put_chain[str(long_put_strike)][0]
        # determine rr and take trade, can speed this up before use
        call_credit = float(call_to_sell["bid"])
        call_debit = float(call_to_buy["ask"])
        put_credit = float(put_to_sell["bid"])
        put_debit = float(put_to_buy["ask"])
        credit = round(((call_credit + put_credit) - (call_debit + put_debit)) * 100)
        risk = round(max((long_call_strike - high) * 100, (low - long_put_strike) * 100) - credit)
        # TESTING ONLY, WOULD OPEN TRADE HERE
        trading_log.write(f"{ticker},iron condor,{credit},{risk},{round(credit/risk, 2)},strikes: {long_put_strike} / {low} // {high} / {long_call_strike}\n")

trading_log.close()
