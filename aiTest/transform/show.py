import model
import numpy as np


dataset = model.DIF_DAY_DATA("stock_data/SH600900.json", 19)

print(dataset[len(dataset) - 1])

import matplotlib.pyplot as plt

plt.rcParams["figure.dpi"] = 500
# plt.ylim((-0.11, 0.11))
# plt.gca().set_aspect(200)
L = np.load("飘飘LL.npy")
plt.plot(dataset[len(dataset) - 1][0])
plt.plot(L / max(L) / 10)
plt.savefig("show")
