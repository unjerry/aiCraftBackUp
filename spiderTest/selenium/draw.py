import numpy as np
import matplotlib.pyplot as plt

# a = np.array([91, 15, 21, 36, 6, 10, 6, 1275, 325, 595])
L = np.load("LL.npy")
plt.rcParams["figure.dpi"] = 500
# plt.gca().set_aspect(1.0)
plt.plot(L, ".-")
# plt.show()
plt.savefig("assa")
