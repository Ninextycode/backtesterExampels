import backtester as bt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class MATrader(bt.Trader):
    def __init__(self, name):
        super().__init__(name)
        self.short_length = 30
        self.long_length = 120

        self.index = 0
        self.sh_last = 0
        self.sh_now = 0
        self.lo_last = 0
        self.lo_now = 0

        self.share_close = np.array([])

    def new_candles_action(self, ticker, candles):
        if ticker == "share_long":
            self.lo_last = self.lo_now
            self.sh_last = self.sh_now
            self.lo_now = \
                self.share_close[- self.long_length:].mean()
            self.sh_now = \
                self.share_close[- self.short_length:].mean()

            self.share_close = np.append(self.share_close, candles[0].close)

            if len(self.share_close) > self.long_length:
                self.work_around_new_candle()


    def work_around_new_candle(self):
        if self.fast_cross_bottom_top():
            self.buy()
        elif self.fast_cross_top_bottom():
            self.sell()

    def fast_cross_bottom_top(self):
        return \
            self.sh_last <= self.lo_last and \
            self.sh_now > self.lo_now

    def fast_cross_top_bottom(self):
        return \
            self.sh_last >= self.lo_last and \
            self.sh_now < self.lo_now

    def buy(self):
        self.make_order(self.create_market_order("share_long",  10 - self.get_portfolio().get("share_long", 0)))

    def sell(self):
        self.make_order(self.create_market_order("share_long", - 10 - self.get_portfolio().get("share_long", 0)))

    def new_tick_action(self, matches, depths):
        self.request_candles("share_long", 1)
        self.index += 1


def run():
    market = bt.Market()

    market.load_history_data("", ["share_long"])

    trader = MATrader("Max")

    market.set_trader(trader)
    trader.set_market(market)

    market.run_full_test()

    print(trader.get_portfolio())

    return trader.get_performance()

def plotter():
    df = pd.read_csv("share.csv")
    ma30 = df["close"].rolling(30).apply(lambda x: x.mean())
    ma120 = df["close"].rolling(120).apply(lambda x: x.mean())

    plt.plot(df["close"], "r", label="price", linewidth=2.0)
    plt.plot(ma30, label="ma30")
    plt.plot(ma120, label="ma120")
    plt.legend()

if __name__ == "__main__":
    run()
