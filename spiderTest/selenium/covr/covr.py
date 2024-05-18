import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

with open("SZ652.json", "r") as file:
    share_data_dict = json.load(file)

name = "泰达股份"
L = np.load(name + "LL.npy")
T = np.load(name + "TT.npy")
TL = []
for it in T:
    TL.append(datetime.strftime(datetime.fromtimestamp(it), "%Y-%m-%d"))
sttime = T[0]
endtime = T[-1]
print(sttime, endtime)
# print(type(share_data_dict["item"]))
share_data_np = np.array(share_data_dict["item"])
# print(share_data_np.shape)
DL = []
NL = []
DT = []
DTT = []
PL = []
rate = 10000
for it in share_data_np:
    if it[0] / 1000 >= sttime and it[0] / 1000 <= endtime:
        # print(it[7])
        # print(np.abs(np.log(it[7] / 100 + 1) * rate))
        if np.abs(np.log(it[7] / 100 + 1) * rate) > 0.03 * rate:
            DL.append(np.abs(np.log(it[7] / 100 + 1) * rate))
        else:
            DL.append(0)
        NL.append((np.log(it[7] / 100 + 1) * rate))
        DT.append(datetime.strftime(datetime.fromtimestamp(it[0] / 1000), "%Y-%m-%d"))


plt.figure(figsize=(100, 10))
plt.rcParams["figure.dpi"] = 500
# plt.gca().set_aspect(0.001)
plt.gca().xaxis.set_major_locator(mdates.DayLocator())
plt.gcf().autofmt_xdate()

plt.plot(TL, L, "g.-")
plt.plot(DT, DL, "r*-")
plt.plot(DT, NL, "b*-")
# plt.show()
plt.savefig(name + "assa")

dct = {}
for i in range(len(DT)):
    dct[DT[i]] = {}
    dct[DT[i]]["x"] = DL[i]
for i in range(len(TL)):
    if TL[i] in dct.keys():
        dct[TL[i]]["y"] = L[i]
X = []
Y = []
for it in dct.values():
    X.append(it["x"])
    Y.append(it["y"])
print("std", np.std(X), np.std(Y))
print("cov", np.cov(X, Y)[0][1] / (np.std(X) * np.std(Y)))
print("covr", np.corrcoef(X, Y)[0][1])
