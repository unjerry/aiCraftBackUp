import numpy as np
import matplotlib.pyplot as plt

np.set_printoptions(linewidth=np.inf)
N = 100
T = np.arange(0, 1, 1 / (2 * N))
Y = np.zeros_like(T)
# for n in range(1, 5):
#     Y += np.sin(2 * np.pi * n * T+n*0.01) / (n * np.pi)
# Y += np.sin(2 * np.pi * T)
Y += np.sin(2 * np.pi * (T**3 + 2 * T**2 + T + 1) * T)

# A = np.fft.fft(Y)
# F = np.fft.fftfreq(n=Y.size, d=1 / (2 * N))
# B = 1 / np.arange(0, N, 1)

# print(T, Y, A, F, np.abs(A), F.size, B.size, sep="\n")

plt.scatter(T, Y)
plt.show()

# plt.scatter(F, np.angle(A) / T.size)
# plt.scatter(F, np.abs(A) / T.size)
# plt.show()
# print(F, A)
# plt.scatter(F[1:], B)
# plt.show()

# plt.scatter(T,Y)
# plt.show()

# plt.scatter(T, Y)
# Y = np.ones_like(T) * np.abs(A[0]) / F.size
# for k in range(1, 5):
#     Y += np.real(
#         np.exp(2j * np.pi * T * k) * A[k] / F.size
#         + np.exp(2j * np.pi * T * (-k)) * A[-k] / F.size
#     )

# plt.scatter(T, Y)
# plt.show()
