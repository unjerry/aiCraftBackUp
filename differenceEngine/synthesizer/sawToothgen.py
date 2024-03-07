import numpy as np
from scipy.io.wavfile import write
from scipy import signal
import matplotlib.pyplot as plt

AUDIO_RATE = 44100
freq = 440
length = 10


t = np.linspace(0, length, length * AUDIO_RATE, dtype=np.float32)

# generate y values for signal
y = signal.sawtooth(2 * np.pi * freq * t)
# save to wave file
write("sawTooth.wav", AUDIO_RATE, y.astype(np.float32))
