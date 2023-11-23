import numpy as np
import wave
import matplotlib.pyplot as plt

# sampling frequency
sf = 48000
# signal time
total_time = 5
# signal frequency
freq = 18000

# generate CW signal
total_point = sf * total_time
t = np.arange(total_point)/sf
# convert the signal to short data type
audio_data = (65536/2-1)*np.cos(2*np.pi*freq*t)
audio_data = audio_data.astype(np.short)

# save audio file
file = wave.open('CW18000.wav', 'wb')
file.setnchannels(1)
file.setsampwidth(2)
file.setframerate(sf)
file.writeframes(audio_data.tobytes())
file.close()

# plot the generated waveform
# this may cost over 20 seconds
plt.figure(1)
plt.plot(t, audio_data)
plt.show()
