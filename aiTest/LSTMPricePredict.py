import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
import pandas_ta as ta

data = yf.download(tickers="SHA:600007", start="2012-03-11", end="2022-07-10")

print(data.head(10))

data["RSI"] = ta.rsi(data.Close, length=15)
data["EMAF"] = ta.ema(data.Close, length=20)
data["EMAM"] = ta.ema(data.Close, length=100)
data["EMAS"] = ta.ema(data.Close, length=150)

data["Target"] = data["Adj Close"] - data.Open
data["Target"] = data["Target"].shift(-1)

data["TargetClass"] = [1 if data.Target[i] > 0 else 0 for i in range(len(data))]
data["TargetNextClose"] = data["Adj Close"].shift(-1)

data.dropna(inplace=True)
data.reset_index(inplace=True)
data.drop(["Volume", "Close", "Date"], axis=1, inplace=True)

data_set = data.iloc[:, 0:11]
pd.set_option("display.max_columns", None)


print(data_set.head(20))

from sklearn.preprocessing import MinMaxScaler

sc = MinMaxScaler(feature_range=(0, 1))
data_set_scaled = sc.fit_transform(data_set)
print(data_set_scaled)

X = []
backCandles = 10
print(data_set_scaled.shape[0])
for j in range(8):
    X.append([])
    for i in range(backCandles, data_set_scaled.shape[0]):
        X[j].append(data_set_scaled[i - backCandles : i, j])

X = np.moveaxis(X, [0], [2])

X, yi = np.array(X), np.array(data_set_scaled[backCandles:, -1])
y = np.reshape(yi, (len(yi), 1))

print(X.shape)
print(y.shape)


splitLimit = int(len(X) * 0.8)
print(splitLimit)
X_train, X_test = X[:splitLimit], X[splitLimit:]
y_train, y_test = y[:splitLimit], y[splitLimit:]
print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)
print(y_train)

