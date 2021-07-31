from obspy import read
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

dataFile = '2021-07-29-mww82-alaska-peninsula-2.miniseed'

st0 = read(dataFile)
st = st0.select(channel='BHZ', location='00')
print(st)

hop_length = 128
n_fft = 256
cmap = 'jet'
bins_per_octave = 12
auto_aspect = False
y_axis = "linear"  # linear or log
fmin = None
fmax = 5.0

data = st[0].data.astype('float32')
sr = int(st[0].stats.sampling_rate)
max_points = int(st[0].stats.npts)
offset = 0

# Waveplot
fig, ax = plt.subplots()
librosa.display.waveshow(data, sr=sr, max_points=max_points,
                         x_axis='time', offset=offset, color='b', ax=ax)
plt.savefig('waveplot.png', bbox_inches='tight', dpi=300)
plt.close()


# Librosa spectrogram
D = librosa.amplitude_to_db(
    np.abs(librosa.stft(data, hop_length=hop_length, n_fft=n_fft)), ref=np.max)


fig, ax = plt.subplots()

img = librosa.display.specshow(D, y_axis=y_axis, sr=sr,
                               hop_length=hop_length, x_axis='time', ax=ax, cmap=cmap, bins_per_octave=bins_per_octave,
                               auto_aspect=auto_aspect)

if fmin is not None:
    fmin0 = fmin
else:
    fmin0 = 0

if fmax is not None:
    fmax0 = fmax
else:
    fmax0 = sr/2

ax.set_ylim([fmin, fmax])
fig.colorbar(img, ax=ax, format="%+2.f dB")
plt.savefig('spectrogram.png', bbox_inches='tight', dpi=300)
plt.close()
