from obspy import read
from obspy.clients.fdsn import Client
from obspy import UTCDateTime
import matplotlib.pyplot as plt

client = Client("IRIS")

origin_time = UTCDateTime("2020-05-15T11:03:27Z")
net = "II"
stn = "PFO"
channel = "BHZ"
st = client.get_waveforms(net, stn, "00", channel,
                          origin_time+40, origin_time+300, attach_response=True)
st_copy = st.copy()
st_copy.remove_response(output="VEL")

# Filtering with a lowpass on a copy of the original Trace
st_copy[0].filter('highpass', freq=10.0, corners=2, zerophase=True)

st.plot(
    outfile="myStream.png",
)

print(st_copy)
st.write(f'{net}-{stn}-{channel}.mseed', format="MSEED")
