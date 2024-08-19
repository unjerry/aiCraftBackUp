import numpy as np
import matplotlib.pyplot as plt

np.set_printoptions(linewidth=np.inf)

T = np.arange(0, 1, 1 / 100)
Y = np.zeros_like(T)
for n in range(1, 100):
    Y += np.sin(2 * np.pi * n * T) / (n * np.pi)

A = np.fft.rfft(Y)
F = np.fft.rfftfreq(n=Y.size, d=1 / 100)
B = 1 / np.arange(0, 50, 1)

print(T, Y, A, F, np.abs(A),F.size,B.size, sep="\n")

plt.scatter(T, Y)
plt.show()

plt.scatter(F, np.abs(A))
plt.show()
plt.scatter(F[1:], B)
plt.show()

# plt.scatter(T,Y)
# plt.show()
