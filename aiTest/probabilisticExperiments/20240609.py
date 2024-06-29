import numpy as np
import scipy
from scipy.stats import rv_continuous, rv_discrete
from distribution import Exp, P, Ga, _01, N


Exp_X = Exp()
Ga_X = Ga(1, 5)
Kai_X = Ga(0.5, 0.5)
P_X = P(5)
_01_X = _01(0.3)
N_X = N(0, 1)
val = N_X.rvs(size=10000)
print(val)


import matplotlib.pyplot as plt


plt.hist(
    val,
    bins=np.arange(int(min(val)) - 1, int(max(val)) + 1, 0.1),
    edgecolor="white",
    density=True,
)
E = np.average(val)
Var = np.average((val - E) ** 2)
print(E, Var, 1, 2)
X = np.arange(int(min(val)) - 1, int(max(val)) + 1, 0.1)
print(X)
Y = N_X._pdf(X)
plt.scatter(X, Y, c="violet")


plt.show()
