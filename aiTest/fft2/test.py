import numpy as np
import matplotlib.pyplot as plt

# 创建一个二维正弦数据
x = np.linspace(0, 10, 16)
y = np.linspace(0, 10, 16)
x, y = np.meshgrid(x, y)
z = np.sin(x) * 0 + np.cos(y) * 0

# 二维傅里叶变换
f = np.fft.ift2(z)
fshift = np.fft.fftshift(f)

# 计算频率
N = z.shape[0]
freq_x = np.fft.fftfreq(N, d=x[1] - x[0])
freq_y = np.fft.fftfreq(N, d=y[1] - y[0])
freq_x, freq_y = np.meshgrid(freq_x, freq_y)

print(freq_x, freq_y)

# 可视化
# plt.subplot(121)
plt.imshow(np.abs(fshift), cmap="gray")
plt.title("FFT Shift")

# plt.subplot(122)
# plt.imshow(
#     np.log(np.abs(fshift) + 1),
#     cmap="gray",
#     extent=[freq_x.min(), freq_x.max(), freq_y.min(), freq_y.max()],
# )
plt.title("Log FFT Shift")
plt.xlabel("Frequency (rad/sample)")
plt.ylabel("Frequency (rad/sample)")

plt.show()
