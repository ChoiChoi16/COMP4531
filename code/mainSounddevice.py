import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import time
import sounddevice as sd

fell = False

# Set the sampling frequency (sf) and duration for each time window
sf = 44100  # Adjust this value based on your microphone's sampling frequency
window_duration = 2  # Duration of each time window in seconds

# Calculate the number of samples per window
window_length = int(sf * window_duration)

# Initialize the audio buffer
audio_buffer = np.zeros(window_length * 2, dtype=np.int16)

# Start recording audio in a stream
stream = sd.InputStream(samplerate=sf, channels=1)

# Start the stream
stream.start()

# Loop to continuously record and process audio in real-time
try:
    while True:
        # Read audio data from the stream
        audio_data_raw = stream.read(window_length)[0]

        # Convert audio data to int16
        audio_data_raw = np.array(audio_data_raw, dtype=np.int16)

        # Concatenate new audio data with the previous buffer
        audio_buffer = np.concatenate((audio_buffer[window_length:], audio_data_raw))

        # Calculate the audio data total length
        n_length = len(audio_buffer)

        # Set the time axis
        t = np.arange(n_length) / sf

        # Get the cosine and sine signals used in demodulation
        freq = 18000
        signal_cos = np.cos(2 * np.pi * freq * t)
        signal_sin = np.sin(2 * np.pi * freq * t)

        # Get a low-pass filter
        b, a = signal.butter(3, 50 / (sf / 2), 'lowpass')

        # Multiply received signal and demodulate signal
        signalI = signal.filtfilt(b, a, audio_buffer * signal_cos)
        signalQ = signal.filtfilt(b, a, audio_buffer * signal_sin)

        # Remove the static vector
        signalI -= np.mean(signalI)
        signalQ -= np.mean(signalQ)

        # Calculate the phase angle
        phase = np.arctan(signalQ / signalI)

        # Unwrap the phase
        phase = np.unwrap(phase * 2) / 2

        # Calculate the wave length and distance
        wave_length = 342 / freq
        distance = phase / (2 * np.pi) * wave_length / 2

        # Calculate acceleration by taking the second derivative of distance
        acceleration = np.gradient(np.gradient(distance, t), t)

        # Fall detection
        fell = max(acceleration) >= 20000

        # Plot the distance
        plt.plot(t, distance)
        plt.xlabel('Time (s)')
        plt.ylabel('Distance (m)')
        plt.show()

        # Plot the acceleration
        plt.plot(t, acceleration)
        plt.xlabel('Time (s)')
        plt.ylabel('Acceleration (m/s^2)')
        plt.show()

        # Alert
        print("")
        if fell:
            print("The user has fallen down! Calling 999...")
        else:
            print("The user is fine.")

except KeyboardInterrupt:
    # Stop the stream when the program is interrupted
    stream.stop()
    stream.close()
 
