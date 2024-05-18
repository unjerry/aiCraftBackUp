import numpy as np

s = np.array(
    [
        [1, 2, 0, 0, 0, 0, 0, 0],
        [5, 7, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]
)
s = np.array(
    [
        [1, 2, 0, 0],
        [5, 7, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        # [0, 0, 0, 0, 0, 0, 0, 0],
        # [0, 0, 0, 0, 0, 0, 0, 0],
        # [0, 0, 0, 0, 0, 0, 0, 0],
        # [0, 0, 0, 0, 0, 0, 0, 0],
    ]
)
t = np.array(
    [
        [1, 5, 0, 0],
        [2, 7, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        # [0, 0, 0, 0, 0, 0, 0, 0],
        # [0, 0, 0, 0, 0, 0, 0, 0],
        # [0, 0, 0, 0, 0, 0, 0, 0],
        # [0, 0, 0, 0, 0, 0, 0, 0],
    ]
)
s2 = s @ s
fs = np.fft.fftfreq(4, s)
rfs = np.fft.fft2(s)
rfsT = np.fft.fft2(s.T)
rfsR = np.fft.fft2(t)
ifs = np.fft.ifft2(fs)
irfs = np.fft.irfft2(rfs)
np.set_printoptions(suppress=True, precision=7, linewidth=1000)
print(s, rfs, irfs, sep="\n", end="\n\n")
print(s2, rfs * rfsT, np.fft.ifft2(rfs * rfs), sep="\n", end="\n\n")
s = np.array(
    [
        [1, 2, 0, 0],
        [1, 2, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]
)
s2 = s @ s.T
fs = np.fft.fftfreq(4, s)
rfs = np.fft.fft2(s)
ifs = np.fft.ifft2(fs)
irfs = np.fft.irfft2(rfs)
print(s, rfs, irfs, sep="\n", end="\n\n")
print(s2, rfs * rfs, np.fft.ifft2(rfs * rfs.T), sep="\n", end="\n\n")

x = np.array([[1, 2, 3, 0], [5, 7, 6, 3], [3, 5, 7, 2], [1, 1, 1, 1]])
y = np.array([[1, 3, 2, 3], [4, 2, 5, 3], [2, 0, 3, 9], [1, 7, 5, 6]])
x2a = x @ x
xp = np.fft.rfft2(x)
x2bp = np.exp(np.log(xp) + np.log(xp)) / 4
x2ap = np.fft.rfft2(x2a)
x2b = np.fft.ifft2(x2bp)
print(np.log(xp))
print(x, xp, x2a, x2b, x2bp, x2ap, x2bp / x2ap, sep="\n")

# z = x @ y
# xp = np.fft.fft2(x)
# yp = np.fft.fft2(y)
# xpT = np.fft.fft2(x.T)
# ypT = np.fft.fft2(y.T)
# zp = np.fft.fft2(z)
# pp = np.exp(np.log(xp) + np.log(yp))
# p = np.fft.ifft2(pp)
# print(x, y, z, p, sep="\n")
# print(xp, xpT, yp, ypT, zp, pp, sep="\n")
