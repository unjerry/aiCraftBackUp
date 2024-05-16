import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np

# 创建一些日期和随机数据
dates = pd.date_range(start="2023-01-01", end="2023-01-10")
print(dates)
data = np.random.rand(len(dates))

# 绘制图形
# fig, ax = plt.subplots()
plt.plot(dates, data)

# 设置日期刻度
# 假设有一个包含每月数据的列表data和对应的日期列表dates

# 设置x轴的日期刻度定位器为每月
plt.gca().xaxis.set_major_locator(mdates.DayLocator())

# 设置x轴的日期格式化器为"%Y-%m"，即年-月
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))

# 旋转x轴的日期标签，使其更易读
plt.gcf().autofmt_xdate()

# 显示图形
plt.show()
