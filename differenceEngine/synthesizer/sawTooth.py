import numpy as np
from scipy.io.wavfile import write
from scipy import signal
import matplotlib.pyplot as plt

AUDIO_RATE = 44100
freq = 440
length = 10

# https://medium.com/@noahhradek/sound-synthesis-in-python-4e60614010da


import numpy as np
from scipy.io.wavfile import write


AUDIO_RATE = 44100
freq = 440
length = 10

# create time values
t = np.linspace(0, length, length * AUDIO_RATE, dtype=np.float32)
# generate y values for signal
for i in range(0, 48 + 1):
    y = signal.sawtooth(2 * np.pi * (freq * 2 ** (i / 12)) * t)
    # save to wave file
    write(f"saw{i}.wav", AUDIO_RATE, y.astype(np.float32))
for i in range(0, 48 + 1):
    y = signal.sawtooth(2 * np.pi * (freq * 2 ** ((i - 48) / 12)) * t)
    # save to wave file
    write(f"saw{i-48}.wav", AUDIO_RATE, y.astype(np.float32))
