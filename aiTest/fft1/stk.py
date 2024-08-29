import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

np.set_printoptions(linewidth=np.inf)
fig = plt.figure(figsize=(100, 5), dpi=300)

df = pd.read_excel("data/600529gai.xlsx", usecols=[0, 1])
df["date"] = pd.to_datetime(df["date"], format="%Y%m%d")
print("dataframe ", df, sep="\n")

plt.scatter(df["date"], df["zuli5_zoom_ma"])
fig.savefig("pe.png")

""" main real value fft proccess """
fft_values = np.fft.fft(df["zuli5_zoom_ma"])
frequencies = np.fft.fftfreq(
    n=len(df["zuli5_zoom_ma"]), d=1 / len(df["zuli5_zoom_ma"])
)
fig = plt.figure(figsize=(20, 10), dpi=300)
plt.stem(frequencies, np.abs(fft_values))
plt.xlabel("Frequency")
plt.ylabel("Amplitude")
plt.title("Fourier Transform Spectrum")
fig.savefig("fft.png")

fig = plt.figure(figsize=(40, 10), dpi=300)
plt.stem(frequencies[0:600], np.abs(fft_values[0:600]))
plt.xlabel("Frequency")
plt.ylabel("Amplitude")
plt.title("Fourier Transform Spectrum")
fig.savefig("fft100.png")

fig = plt.figure(figsize=(20, 10), dpi=300)
plt.stem(frequencies, np.angle(fft_values))
plt.xlabel("Frequency")
plt.ylabel("Amplitude")
plt.title("Fourier Transform Spectrum")
fig.savefig("fftangle.png")


fig = plt.figure(figsize=(100, 10), dpi=300)
T = np.arange(0, 1.2, (1 / (frequencies.size)))
Y = np.ones_like(T) * np.abs(fft_values)[0] / len(df["zuli5_zoom_ma"])
print(Y[0])
for k in range(100, 300):
    Y += np.real(
        np.exp(2j * np.pi * T * k) * fft_values[k] / frequencies.size
        + np.exp(2j * np.pi * T * (-k)) * fft_values[-k] / frequencies.size
    )

plt.scatter(
    np.arange(0, df["zuli5_zoom_ma"].size, 1), df["zuli5_zoom_ma"]
)
plt.scatter(np.arange(0, Y.size, 1), Y)
print(T.size, df["zuli5_zoom_ma"].size, frequencies.size)
fig.savefig("pe_with_wave30.png")
