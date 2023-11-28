import numpy as np
from scipy import signal
import wave
import matplotlib.pyplot as plt

# read audio file recorded by Raspberry pi
file = wave.open('FallFinal.wav', 'rb')
# get sampling frequency
sf = file.getframerate()
# get audio data total length
n_length = file.getnframes()
# read audio data
audio_data_raw = file.readframes(n_length)
# transfer to python list
audio_data_raw = list(audio_data_raw)
# transfer to numpy array
audio_data_raw = np.asarray(audio_data_raw, np.int8)
# set the data type to int16
audio_data_raw.dtype = 'int16'
# calculate audio length in second
audio_data_raw_total_time = n_length/sf
# close the file
file.close()

# cut the middle part of the audio data
time_offset = 2
total_time = np.int32(np.ceil(audio_data_raw_total_time - time_offset - 2))
total_point = total_time * sf
time_offset_point = time_offset * sf
audio_data = audio_data_raw[range(time_offset_point,time_offset_point+total_point)]

# set frequency
freq = 18000
# calculate time t
t = np.arange(total_point)/sf
# get the cos and sin used in demodulation
signal_cos = np.cos(2*np.pi*freq*t)
signal_sin = np.sin(2*np.pi*freq*t)
# get a low-pass filter
b, a = signal.butter(3, 50/(sf/2), 'lowpass')
# multiply received signal and demodulate signal
signalI = signal.filtfilt(b, a, audio_data*signal_cos)
signalQ = signal.filtfilt(b, a, audio_data*signal_sin)
# remove the static vector
signalI = signalI - np.mean(signalI)
signalQ = signalQ - np.mean(signalQ)
# calculate the phase angle
phase = np.arctan(signalQ/signalI)
# plot the IQ figure
plt.plot(signalI, signalQ)
plt.xlabel('I')
plt.ylabel('Q')
plt.show()
# plot the original phase
plt.plot(t, phase)
plt.xlabel('t/s')
plt.show()
# unwrap the phase
phase = np.unwrap(phase*2)/2

# fall detection
fallen_duration = 0
for i in phase:
    if (i < -60):
        print("fall for", fallen_duration, "ms")
        fallen_duration += 1
        if (fallen_duration > 120):
            break

# plot the unwraped phase
plt.plot(t, phase)
plt.show()
# calculate the wave length
wave_length = 342/freq
# calculate the distance
distance = phase/2/np.pi*wave_length/2
# plot the distance
plt.plot(t, distance)
plt.xlabel('time/s')
plt.ylabel('distance/m')
plt.show()
