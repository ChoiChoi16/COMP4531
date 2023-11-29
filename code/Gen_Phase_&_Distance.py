import numpy as np
from scipy import signal
import wave
import matplotlib.pyplot as plt
import time

fell = False
filename = input("what is the filename of the wav audio?")
filename = filename + '.wav'

# Read audio file recorded by Raspberry Pi using a context manager
with wave.open(filename, 'rb') as file:
    # Get sampling frequency and audio data total length
    sf = file.getframerate()
    n_length = file.getnframes()

    # Read audio data and convert to int16
    audio_data_raw = np.frombuffer(file.readframes(n_length), dtype=np.int16)


# calculate audio length in second
audio_data_raw_total_time = n_length/sf


# cut the middle part of the audio data
time_offset = 2
time_offset_point = int(time_offset * sf)
total_time = np.int32(np.ceil(audio_data_raw_total_time - time_offset - 2))
total_point = total_time * sf
audio_data = audio_data_raw[range(time_offset_point,time_offset_point+total_point)]

# set frequency and calculate time t
freq = 18000
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
signalI -= np.mean(signalI)
signalQ -= np.mean(signalQ)

# calculate the phase angle
phase = np.arctan(signalQ/signalI)


# plot the IQ figure
'''plt.plot(signalI, signalQ)
plt.xlabel('I')
plt.ylabel('Q')
plt.show()'''
# plot the original phase
'''plt.plot(t, phase)
plt.xlabel('t/s')
plt.show()'''


# unwrap the phase
phase = np.unwrap(phase*2)/2


# plot the unwraped phase
'''plt.plot(t, phase)
plt.show()'''


# calculate the wave length and distance
wave_length = 342/freq
distance = phase/2/np.pi*wave_length/2

# Calculate acceleration by taking the second derivative of distance
acceleration = np.gradient(np.gradient(distance, t), t)


# fall detection
#fall_duration = np.sum(phase >= 100)
#fell = fall_duration >= 120000
#fall_duration = np.sum(acceleration >= 1000)
fell = max(acceleration) >= 20000
#print(fall_duration)
#print(acceleration)
#print(max(acceleration))


# plot the distance
#plt.plot(t, distance)
#plt.xlabel('time/s')
#plt.ylabel('distance/m')
#plt.show()

# Plot the acceleration
#plt.plot(t, acceleration)
#plt.xlabel('Time (s)')
#plt.ylabel('Acceleration (m/s^2)')
#plt.show()


# alert
print("")
if fell:
    print("user has fell down! Calling 999...")
else:
    print("user is fine.")
