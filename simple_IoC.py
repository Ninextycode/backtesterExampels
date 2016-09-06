import backtester as bt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class MATrader(bt.Trader):
    def __init__(self, name):
        super().__init__(name)
        self.index = 0

    def new_candles_action(self, ticker, candles):
        pass

    def new_tick_action(self, matches, depths):
        if self.index == 0:
            self.make_order(self.create_IoC_order("share_40000", 100, 40100))
            #self.make_order(self.create_IoC_order("share_40000", -100, 39800))
        self.index += 1


def run():
    market = bt.Market()

    market.load_history_data("", ["share_40000"])

    trader = MATrader("Max")

    market.set_trader(trader)
    trader.set_market(market)

    market.run_full_test()

    print(trader.get_portfolio())

    return trader.get_performance()

def plotter():
    df = pd.read_csv("share_40000.csv")
    ma30 = df["close"].rolling(30).apply(lambda x: x.mean())
    ma120 = df["close"].rolling(120).apply(lambda x: x.mean())

    plt.plot(df["close"], "r", label="price", linewidth=2.0)
    plt.plot(ma30, label="ma30")
    plt.plot(ma120, label="ma120")
    plt.legend()

if __name__ == "__main__":
    run()
