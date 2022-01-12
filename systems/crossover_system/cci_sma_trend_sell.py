"""A simple moving average cross or cci strategy. This strategy buys when the cci goes from below to above 100, or when the fast sma crosses above the slow sma. It sells when the cci goes from above to below -100, or when the slow sma crosses above the fast sma. Only sells with a longer term trend. If already in a position, it either holds if given the same signal, or reverses the position if given the opposite. There are no stops. Cope."""

# TODO: fix imports
from ..setup.futures_system import FuturesSystem
from ...indicators.simple_indicators import sma 
from ...indicators.cci import cci_at_t

class CciSmaSystemTrendSell(FuturesSystem):
    """Takes some parameters and performs tests"""
    def __init__(self, symbol, contract_multiplier, margin_req, cci_length, fast_avg_length, slow_avg_length, trend_length, safety_margin, start_date=None, end_date=None, linedict=None):

        super().__init__(symbol, contract_multiplier, margin_req, safety_margin, start_date, end_date, linedict)
        #adjustable values
        self.fast_avg = fast_avg_length
        self.slow_avg = slow_avg_length
        self.trend_length = trend_length
        self.cci_length = cci_length

        #working values
        if self.time < max(self.cci_length, self.slow_avg, self.trend_length, self.fast_avg):
            self.time = max(self.cci_length, self.slow_avg, self.trend_length, self.fast_avg) + 1

    def __repr__(self) -> str:
        return f"Sell CCI Trend ({self.fast_avg}) ({self.slow_avg}) ({self.trend_length}) ({self.cci_length})"

    def _check_sma_buy(self):
        if (sma(self.linedict, self.fast_avg, self.time-1) < sma(self.linedict, self.slow_avg, self.time-1)) and (sma(self.linedict, self.fast_avg, self.time) > sma(self.linedict, self.slow_avg, self.time)):
            return True 
        return False 

    def _check_sma_sell(self):
        if (sma(self.linedict, self.fast_avg, self.time-1) > sma(self.linedict, self.slow_avg, self.time-1)) and (sma(self.linedict, self.fast_avg, self.time) < sma(self.linedict, self.slow_avg, self.time)):
            return True 
        return False

    def _check_cci_buy(self):
        if cci_at_t(self.linedict, self.cci_length, self.time-1) < 100 and cci_at_t(self.linedict, self.cci_length, self.time) > 100:
            return True
        return False 

    def _check_cci_sell(self):
        if cci_at_t(self.linedict, self.cci_length, self.time-1) > -100 and cci_at_t(self.linedict, self.cci_length, self.time) < -100:
            return True
        return False

    def _check_trend_confirm_buy(self):
        if sma(self.linedict, self.trend_length, self.time - 1) < sma(self.linedict, self.trend_length, self.time):
            return True 
        return False 

    def _check_trend_confirm_sell(self):
        if sma(self.linedict, self.trend_length, self.time - 1) > sma(self.linedict, self.trend_length, self.time):
            return True 
        return False 

    def _check_trend_change_buy(self):
        change = (sma(self.linedict, self.trend_length, self.time - 2) > sma(self.linedict, self.trend_length, self.time - 1)) and (sma(self.linedict, self.trend_length, self.time - 1) < sma(self.linedict, self.trend_length, self.time))
        confirm = sma(self.linedict, self.fast_avg, self.time) > sma(self.linedict, self.slow_avg, self.time)
        if change and confirm:
            return True 
        return False 

    def _check_trend_change_sell(self):
        change = (sma(self.linedict, self.trend_length, self.time - 2) < sma(self.linedict, self.trend_length, self.time - 1)) and (sma(self.linedict, self.trend_length, self.time - 1) > sma(self.linedict, self.trend_length, self.time))
        confirm = sma(self.linedict, self.fast_avg, self.time) < sma(self.linedict, self.slow_avg, self.time)
        if change and confirm:
            return True 
        return False 

    def check_buy(self):
        buy = self._check_cci_buy() or self._check_sma_buy()
        if buy and self.position == "NONE":
            self.position = "LONG"
            if self._check_cci_buy():
                self.order_price = self.linedict[self.time][4]
            else:
                self.order_price = self.linedict[self.time][1]
            self.last_difference = self.order_price
            return True
        elif buy and self.position == "SHORT":
            self.profit += ((self.order_price - self.linedict[self.time][1]) * self.position_size * self.contract_multiplier)
            self.position = "LONG"
            if self._check_cci_buy():
                self.order_price = self.linedict[self.time][4]
            else:
                self.order_price = self.linedict[self.time][1] 
            self.last_difference = self.order_price
            return True 
        return False

    def check_sell(self):
        sell = ((self._check_cci_sell() or self._check_sma_sell()) and self._check_trend_confirm_sell()) or self._check_trend_change_sell()
        close = self._check_cci_sell() or self._check_sma_sell()
        if sell and self.position == "NONE":
            self.position = "SHORT"
            if self._check_cci_sell():
                self.order_price = self.linedict[self.time][4]
            else:
                self.order_price = self.linedict[self.time][1]
            self.last_difference = self.order_price
            return True
        elif sell and self.position == "LONG":
            self.profit += ((self.linedict[self.time][1] - self.order_price) * self.position_size * self.contract_multiplier)
            self.position = "SHORT"
            if self._check_cci_sell():
                self.order_price = self.linedict[self.time][4]
            else:
                self.order_price = self.linedict[self.time][1] 
            self.last_difference = self.order_price
            return True 
        elif close and self.position == "LONG":
            self.profit += ((self.linedict[self.time][1] - self.order_price) * self.position_size * self.contract_multiplier)
            self.position = "NONE"
            self.order_price = 0.0
            self.last_difference = 0.0
            return True 
        return False 

    def run_test(self):
        while self.time < self.end_time:
            self.check_acct()
            #self.set_position_size()
            self.check_values()
            self.check_buy()
            self.check_sell()
            if self.account.value < 0.0:
                self.viable = False
                break
            self.time += 1

    def write_file(self):
        c = '_'
        name = self.symbol + c + str(self.fast_avg) + c + str(self.slow_avg) + c + str(self.trend_length) + c + str(self.cci_length) + "_trend_sell_report.txt"
        outfile = open(name, 'w') 
        outfile.write("Starting Value: 8500.07\n\n")
        outfile.write(f"\nDrawdowns: {self.drawdowns}\nMax: {self.max_drawdown}\n")
        outfile.write(f"Profit: {self.profit}\n")
        outfile.write(f"Ending Value: {self.account.value}")
        outfile.close()
