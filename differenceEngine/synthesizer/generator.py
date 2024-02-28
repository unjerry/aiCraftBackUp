import librosa
import soundfile
import os
from pathlib import Path
import numpy

DESCRIPTOR_32BIT = "FLOAT"

wav_path = "E:\\workspace-git\\remotegithub\\others\\aiCraft\\differenceEngine\\synthesizer\\piano_c4.wav"


def get_audio_data(wav_path: str):
    audio_data, framerate_hz = soundfile.read(wav_path)
    array_shape = audio_data.shape
    if len(array_shape) == 1:
        channels = 1
    else:
        channels = array_shape[1]
    return audio_data, framerate_hz, channels


audio_data, sample_rate_hz, channels = get_audio_data(wav_path)

y, sr = librosa.load(wav_path, sr=sample_rate_hz, mono=channels == 1)
file_name = os.path.splitext(os.path.basename(wav_path))[0]
folder_containing_wav = Path(wav_path).parent.absolute()
cache_folder_path = Path(folder_containing_wav, file_name)
# if clear_cache and cache_folder_path.exists():
#     shutil.rmtree(cache_folder_path)
if not cache_folder_path.exists():
    print("Generating samples for each key")
    os.mkdir(cache_folder_path)

tones = [i - 48 for i in range(96+1)]

for i, tone in enumerate(tones):
    cached_path = Path(cache_folder_path, "{}.wav".format(tone))
    if Path(cached_path).exists():
        print("Loading note {} out of {} for ".format(i + 1, len(tones)))
        sound, sr = librosa.load(cached_path, sr=sample_rate_hz, mono=channels == 1)
        if channels > 1:
            # the shape must be [length, 2]
            sound = numpy.transpose(sound)
    else:
        print("Transposing note {} out of {} for".format(i + 1, len(tones)))
        if channels == 1:
            print(y, len(y))
            sound = librosa.effects.pitch_shift(y=y, sr=sr, n_steps=tone)
        else:
            new_channels = [
                librosa.effects.pitch_shift(y=y[i], sr=sr, n_steps=tone)
                for i in range(channels)
            ]
            sound = numpy.ascontiguousarray(numpy.vstack(new_channels).T)
        soundfile.write(cached_path, sound, sample_rate_hz, DESCRIPTOR_32BIT)
