"""A simple simple moving average trend following strategy. No stops, no bullshit. Cope."""

# TODO: fix imports
from ..setup.futures_system import FuturesSystem
from ...indicators.simple_indicators import sma 

class SmaTrend(FuturesSystem):
    def __init__(self, symbol, contract_multiplier, margin_req, length, safety_margin, start_date=None, end_date=None, linedict=None):

        super().__init__(symbol, contract_multiplier, margin_req, safety_margin, start_date, end_date, linedict)

        self.length = length 

        if self.time < self.length:
            self.time = self.length + 1

    def __repr__(self) -> str:
        return f"Sma Trend ({self.length})"

    def check_buy(self):
        buy = (sma(self.linedict, self.length, self.time - 2) < sma(self.linedict, self.length, self.time - 1)) and (sma(self.linedict, self.length, self.time - 1) < sma(self.linedict, self.length, self.time))
        if buy and self.position == "NONE":
            self.position = "LONG"
            self.order_price = self.linedict[self.time][1]
            self.last_difference = self.order_price
            return True
        elif buy and self.position == "SHORT":
            self.profit += ((self.order_price - self.linedict[self.time][1]) * self.position_size * self.contract_multiplier)
            self.position = "LONG"
            self.order_price = self.linedict[self.time][1] 
            self.last_difference = self.order_price
            return True 
        return False

    def check_sell(self):
        sell = (sma(self.linedict, self.length, self.time - 2) > sma(self.linedict, self.length, self.time - 1)) and (sma(self.linedict, self.length, self.time - 1) > sma(self.linedict, self.length, self.time))
        if sell and self.position == "NONE":
            self.position = "SHORT"
            self.order_price = self.linedict[self.time][1]
            self.last_difference = self.order_price
            return True
        elif sell and self.position == "LONG":
            self.profit += ((self.linedict[self.time][1] - self.order_price) * self.position_size * self.contract_multiplier)
            self.position = "SHORT"
            self.order_price = self.linedict[self.time][1] 
            self.last_difference = self.order_price
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
        name = self.symbol + c + str(self.length) + "_sma_report.txt"
        outfile = open(name, 'w') 
        outfile.write("Starting Value: 8500.07\n\n")
        outfile.write(f"\nDrawdowns: {self.drawdowns}\nMax: {self.max_drawdown}\n")
        outfile.write(f"Profit: {self.profit}\n")
        outfile.write(f"Ending Value: {self.account.value}")
        outfile.close()
