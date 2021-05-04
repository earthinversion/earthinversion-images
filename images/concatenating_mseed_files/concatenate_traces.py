import glob, os
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [10,6]
plt.rcParams.update({'font.size': 18})
plt.style.use('seaborn')
from obspy import read, Stream
import matplotlib.dates as mdates
from matplotlib import dates
from matplotlib.colors import Normalize
from spectrogram_obspy_modified import compute_spectrogram

mseed_data_comb = "appended_out.mseed"
concatenate_traces = False
if concatenate_traces:
    mseed_data = glob.glob(os.path.join("data", "*.mseed"))

    datarange = np.arange(0,15, dtype=int)
    stZ = read(mseed_data[datarange[0]])
    mytrace = stZ[0]

    starttime0 = mytrace.stats.starttime
    endtime0 = mytrace.stats.endtime

    for i,trdata in enumerate(mseed_data[datarange[1]:datarange[-1]]):
        st = read(trdata)
        if i==0:
            oldend = endtime0
        print(f"Reading trace {i+2}: {trdata}, range: {st[0].stats.starttime}-{st[0].stats.endtime}, jump: {st[0].stats.starttime-oldend} second")
        tr = st[0]

        mytrace+=tr
        oldend = tr.stats.endtime

    mystream = Stream(traces=[mytrace])
    for tr in mystream:
        if isinstance(tr.data, np.ma.masked_array):
            tr.data = tr.data.filled(0)

    ## I want the final sampling rate to be 1Hz
    mystream.interpolate(sampling_rate=mystream[0].stats.sampling_rate/mystream[0].stats.sampling_rate,starttime=starttime0) #to deal with missing data

    #abort downsampling in case of changing end times (strict_length=true)
    # mystream[0].decimate(factor=10, strict_length=False, no_filter=False) #lowpass filter is applied to ensure no aliasing artifacts are introduced
    # mystream[0].decimate(factor=4, strict_length=False, no_filter=False)



    mystream.write(mseed_data_comb, format="MSEED")  


## Read back and plot
newMseed = read(mseed_data_comb)
print(newMseed)
fig, ax = plt.subplots(1,1)
ax.plot(newMseed[0].times('matplotlib'), newMseed[0].data, lw=0.5, color='k')

fig.autofmt_xdate()
plt.tight_layout()
plt.savefig('new-mseed-data.png', bbox_inches='tight', dpi=300)
plt.close('all')


# ## Plot spectrogram
# fig, axx = plt.subplots(1,1, figsize=(10,4))
# total_length = newMseed[0].data.shape[0]
# wlength = int(total_length/12) #window length for fft
# newMseed[0].spectrogram(log=False, wlen=wlength,show=False, axes=axx, cmap='jet', dbscale=True) #wlen for the trade off between freq and time
# ymin, ymax = axx.get_ylim()
# xmin, xmax = axx.get_xlim()

# print(xmin, xmax, ymin, ymax)
# axx.set_xlim([xmin+wlength, xmax-wlength])
# axx.set_title('Spectrogram')
# axx.set_xlabel('Time in sec')
# axx.set_ylabel('Frequency (Hz)')
# plt.tight_layout()
# plt.savefig('spectrogram_plot.png', bbox_inches='tight', dpi=300)
# plt.close('all')


## Plot spectrogram
fig, axx = plt.subplots(1,1, figsize=(10,4))
total_length = newMseed[0].data.shape[0]
wlength = int(total_length/12) #window length for fft

specgram, freq, time = compute_spectrogram(newMseed[0].data,samp_rate=newMseed[0].stats.sampling_rate, wlen=wlength, dbscale=True) #wlen for the trade off between freq and time

## Normalize the color map
vmin = specgram.min()
vmax = specgram.max() 
if vmin<0:
    vmin = 0
norm = Normalize(vmin, vmax, clip=True)
axx.set_yscale('log')
cscale = axx.pcolormesh(time, freq, specgram, norm=norm, cmap='jet')
# Log scaling for frequency values (y-axis)

axx.set_title('Spectrogram')
axx.set_xlabel('Time in seconds')
axx.set_ylabel('Frequency (Hz)')
cbar = fig.colorbar(cscale, extend='max')
cbar.set_label('Amplitude in dbscale')
plt.tight_layout()
plt.savefig('spectrogram_plot2.png', bbox_inches='tight', dpi=300)
plt.close('all')