# Liam Murphy

import warnings

from pandas.io import json
warnings.filterwarnings("ignore")
import pandas as pd
import matplotlib.pyplot as plt 
plt.style.use("fivethirtyeight")
from matplotlib import rcParams
rcParams["figure.figsize"] = 10, 6
import json 
import datetime

class StoredArima:
    def __init__(self, fitted, newest_datetime):
        self.fitted = fitted
        self.newest_datetime = newest_datetime

def json_to_dataframe(ticker : str):
    path = "/Users/liammurphy/Documents/Personal/Projects/Python_Projects/trading/data/equities/" + ticker + ".json"
    candles = pd.DataFrame((dict(json.load(open(path))))["candles"])
    actual_dts = [datetime.datetime.fromtimestamp(mils / 1000) for mils in candles["datetime"]]
    candles["datetime"] = actual_dts
    candles.set_index("datetime", inplace=True)
    # debug
    # print(candles)
    return candles

def plot_close_price(ticker : str, candles : pd.DataFrame):
    plt.figure(figsize=(10,6))
    plt.grid(True)
    plt.xlabel("Dates")
    plt.ylabel("Close")
    plt.plot(candles["close"])
    plt.title(ticker +" Close Price")
    plt.show()

def create_auto_arima(train_closes : pd.Series):
    model_autoARIMA = auto_arima(train_closes, start_p=0, start_q=0,
                      test='adf',       # use adftest to find             optimal 'd'
                      max_p=5, max_q=5, # maximum p and q
                      m=1,              # frequency of series
                      d=None,           # let model determine 'd'
                      seasonal=False,   # No Seasonality
                      start_P=0, 
                      D=0, 
                      trace=True,
                      error_action='ignore',  
                      suppress_warnings=True, 
                      stepwise=True)
                      
    # debug                  
    # print(model_autoARIMA.summary())
    # check that model is appropriate
    # model_autoARIMA.plot_diagnostics(figsize=(15,8))
    # plt.show()
    model_autoARIMA.fit(train_closes)
    return model_autoARIMA

def sanity_test_forecast(ticker : str):
    candles = json_to_dataframe(ticker)
    closes = candles["close"]
    # may change ranges for test and train data, we shall seeeee
    cutoff = int(len(closes) * 0.90)
    train_closes, test_closes = closes[:cutoff], closes[cutoff:]
    fitted = create_auto_arima(train_closes)
    # change n_periods
    fc, conf = fitted.predict(n_periods=len(test_closes), return_conf_int=True)  # 95% confidence
    fc_series = pd.Series(fc, index=test_closes.index)
    lower_series = pd.Series(conf[:, 0], index=test_closes.index)
    upper_series = pd.Series(conf[:, 1], index=test_closes.index)
    plt.figure(figsize=(12,5), dpi=100)
    plt.plot(train_closes, label='training')
    plt.plot(test_closes, color = 'blue', label='Actual Stock Price')
    plt.plot(fc_series, color = 'orange',label='Predicted Stock Price')
    plt.fill_between(lower_series.index, lower_series, upper_series, 
                    color='k', alpha=.10)
    plt.title(ticker + ' Stock Price Prediction')
    plt.xlabel('Time')
    plt.ylabel('Actual Stock Price')
    plt.legend(loc='upper left', fontsize=8)
    plt.show()

def forecast_each_week_test(ticker : str):
    candles = json_to_dataframe(ticker)
    closes = candles["close"]
    # may change ranges for test and train data, we shall seeeee
    cutoff = int(len(closes) * 0.90)
    train_closes, test_closes = closes[:cutoff], closes[cutoff:]
    fitted = create_auto_arima(train_closes)
    pred_length = 5
    fc_list = []
    lower_list = []
    upper_list = []
    index_list = []
    for i in range(len(test_closes) // pred_length):
        fc, conf = fitted.predict(n_periods=pred_length, return_conf_int=True)  # 95% confidence
        
        fc_list.extend(fc)
        lower_list.extend(conf[:, 0])
        upper_list.extend(conf[:, 1])
        index_list.extend(test_closes.index[i * pred_length: (i + 1) * pred_length])
        fitted.update(test_closes[i * pred_length: (i + 1) * pred_length])

    fc_series = pd.Series(fc_list, index=index_list)
    lower_series = pd.Series(lower_list, index=index_list)
    upper_series = pd.Series(upper_list, index=index_list)
    # plt.plot(train_closes, label='training')
    plt.figure(figsize=(15,8), dpi=100)
    plt.plot(test_closes, color = 'blue', label='Actual Stock Price')
    plt.plot(fc_series, color = 'orange',label='Predicted Stock Price')
    plt.fill_between(lower_series.index, lower_series, upper_series, 
                        color='k', alpha=.10)
    plt.title(ticker + ' Stock Price Prediction')
    plt.xlabel('Time')
    plt.ylabel('Actual Stock Price')
    plt.legend(loc='upper left', fontsize=8)
    plt.show()

def test_forecast_accuracy(ticker : str):
    candles = json_to_dataframe(ticker)
    closes = candles["close"]
    # may change ranges for test and train data, we shall seeeee
    cutoff = int(len(closes) * 0.90)
    train_closes, test_closes = closes[:cutoff], closes[cutoff:]
    fitted = create_auto_arima(train_closes)
    pred_length = 5
    hits = 0
    for i in range(len(test_closes) // pred_length):
        fc, conf = fitted.predict(n_periods=pred_length, return_conf_int=True)  # 95% confidence
        low = conf[4, 0]
        high = conf[4, 1]
        close = test_closes[((i + 1) * pred_length) - 1]
        if close > low and close < high:
            hits += 1
        fitted.update(test_closes[i * pred_length: (i + 1) * pred_length])
    return len(closes), len(test_closes) // pred_length, (hits / (len(test_closes) // pred_length))
