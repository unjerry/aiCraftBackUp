import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import torch

np.set_printoptions(linewidth=np.inf)
fig = plt.figure(figsize=(100, 5), dpi=300)

df = pd.read_excel("data/500.xlsx", usecols=[0, 14])
df["date"] = pd.to_datetime(df["date"], format="%Y%m%d")
print("dataframe ", df, sep="\n")

plt.scatter(df["date"], df["pb_earning_probability"])
fig.savefig("pe.png")

""" main real value fft proccess """
fft_values = np.fft.fft(df["pb_earning_probability"])
frequencies = np.fft.fftfreq(
    n=len(df["pb_earning_probability"]), d=1 / len(df["pb_earning_probability"])
)
fig = plt.figure(figsize=(20, 10), dpi=300)
plt.stem(frequencies, np.abs(fft_values))
plt.xlabel("Frequency")
plt.ylabel("Amplitude")
plt.title("Fourier Transform Spectrum")
fig.savefig("fft.png")

fig = plt.figure(figsize=(20, 10), dpi=300)
plt.stem(frequencies, np.angle(fft_values))
plt.xlabel("Frequency")
plt.ylabel("Amplitude")
plt.title("Fourier Transform Spectrum")
fig.savefig("fftangle.png")


fig = plt.figure(figsize=(20, 10), dpi=300)
T = np.arange(0, 1.2, (1 / (frequencies.size)))
Y = np.ones_like(T) * np.abs(fft_values)[0] / len(df["pb_earning_probability"])
print(Y[0])
for k in range(1, 3):
    Y += np.real(
        np.exp(2j * np.pi * T * k) * fft_values[k] / frequencies.size
        + np.exp(2j * np.pi * T * (-k)) * fft_values[-k] / frequencies.size
    )

plt.scatter(
    np.arange(0, df["pb_earning_probability"].size, 1), df["pb_earning_probability"]
)
plt.scatter(np.arange(0, Y.size, 1), Y)
print(T.size, df["pb_earning_probability"].size, frequencies.size)
fig.savefig("pe_with_wave3.png")
