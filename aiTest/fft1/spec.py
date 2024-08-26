import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

np.set_printoptions(linewidth=np.inf)

# 创建示例DataFrame
data = {
    "date": pd.date_range(start="2022-01-01", periods=100, freq="D"),
    "value": np.sin(np.arange(0, 20, 20 / 100)),
}  # 创建一个简单的正弦波时间序列列
df = pd.DataFrame(data)

print(df)
plt.scatter(data["date"], data["value"])
plt.show()

# 执行傅里叶变换
fft_values = np.fft.rfft(df["value"])
n = len(df["value"])
frequencies = np.fft.rfftfreq(n, 20 / 100)

# 绘制频谱图
plt.figure(figsize=(12, 6))
plt.stem(frequencies, np.abs(fft_values))
plt.xlabel("Frequency")
plt.ylabel("Amplitude")
plt.title("Fourier Transform Spectrum")
plt.show()

# 寻找频率成分的主要峰值
peak_frequencies = np.abs(fft_values).argsort()[-5:][
    ::-1
]  # 找到幅度最大的前5个频率成分
print("Peak frequencies:", np.abs(frequencies[peak_frequencies]))

# 判断周期性
threshold = 0.1  # 设置阈值，用于判断周期性
if np.any(np.abs(frequencies[peak_frequencies]) > threshold):
    print("具有周期性")
else:
    print("不具有周期性")
