import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# a = np.array([91, 15, 21, 36, 6, 10, 6, 1275, 325, 595])
name = "飘飘"
L = np.load(name + "LL.npy")
T = np.load(name + "TT.npy")
TL = []
for it in T:
    # print(it)
    TL.append(datetime.strftime(datetime.fromtimestamp(it), "%Y-%m-%d"))
# print(TL)
plt.figure(figsize=(100, 10))
plt.rcParams["figure.dpi"] = 500
# plt.gca().set_aspect(0.001)
plt.gca().xaxis.set_major_locator(mdates.DayLocator())

# 设置x轴的日期格式化器为"%Y-%m"，即年-月
# plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))

# 旋转x轴的日期标签，使其更易读
plt.gcf().autofmt_xdate()
plt.plot(TL, L, ".-")
# plt.show()
plt.savefig(name + "assa")
