import numpy as np
from numpy import inf
from scipy.special import gamma
from scipy.stats import rv_continuous, rv_discrete


class Exp(rv_continuous):
    "Exponential distribution"

    def __init__(self):
        super().__init__(a=0)

    def _pdf(self, x):
        return np.exp(-x)


class Ga(rv_continuous):
    "Exponential distribution"

    def __init__(self, alpha, lamda):
        self.alpha = alpha
        self.lamda = lamda
        super().__init__(a=0)

    def _pdf(self, x):
        return (
            (self.lamda**self.alpha)
            * (x ** (self.alpha - 1))
            * np.exp(-self.lamda * x)
            / gamma(self.alpha)
        )


class N(rv_continuous):
    def __init__(self, mu, sig2):
        self.mu = mu
        self.sig2 = sig2
        super().__init__()

    def _pdf(self, x):
        return (np.exp(-((x - self.mu) ** 2) / (2 * self.sig2))) / (
            np.sqrt(2 * np.pi * self.sig2)
        )


class P(rv_discrete):
    "Poisson distribution"

    def __init__(self, l):
        self.l = l
        super().__init__()

    def _pmf(self, k):
        return (np.exp(-self.l) * self.l**k) / gamma(k + 1)


class _01(rv_discrete):
    "0-1 distribution"

    def __init__(self, p):
        self.p = p
        super().__init__(a=0, b=1)

    def _pmf(self, k):
        return (self.p**k) * ((1 - self.p) ** (1 - k))
