import simple_limit as s_ioc
import matplotlib.pyplot as plt
import pandas as pd

df = s_ioc.run()

performance = pd.DataFrame(df)
performance["lv"] = performance["lv"]/100
performance["money"] = performance["money"]/100

f1 = plt.figure()
f2 = plt.figure()

ax1 = f1.add_subplot(111)
ax2 = f2.add_subplot(111)

share = pd.read_csv("share.csv")

share_ma = pd.DataFrame()

share_ma["close"] = share["close"]
share_ma["ma30"] = share["close"].rolling(30).apply(lambda x : x.mean())
share_ma["ma120"] = share["close"].rolling(120).apply(lambda x : x.mean())


performance.plot(ax=ax1, subplots=True)

share_ma.plot(ax=ax2, grid=True)

plt.show()