import threading
import time
import pyaudio
import wave

def play_wav_file(file_path = 'CW18000.wav'):
    chunk = 1024
    wf = wave.open(file_path, 'rb')

    # Initialize Pyaudio
    p = pyaudio.PyAudio()

    # Open the audio stream
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # Read and play the audio file in chunks
    data = wf.readframes(chunk)
    while data:
        stream.write(data)
        data = wf.readframes(chunk)

    # Close the stream and terminate Pyaudio
    stream.stop_stream()
    stream.close()
    p.terminate()

def record_audio(record_path = 'record.wav', duration=5, sample_rate=48000, channels=1):
    chunk = 1024
    format = pyaudio.paInt16

    # Initialize Pyaudio
    p = pyaudio.PyAudio()

    # Open the audio stream
    stream = p.open(format=format,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=chunk)

    print("Recording started...")

    # Create a buffer to store the recorded data
    frames = []

    # Record audio for the specified duration
    for _ in range(0, int(sample_rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    print("Recording finished.")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded data as a WAV file
    wf = wave.open(record_path, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(sample_rate)
    wf.writeframes(b''.join(frames))
    wf.close()

# Create threads for each function
thread1 = threading.Thread(target=play_wav_file)
thread2 = threading.Thread(target=record_audio)

# Start the threads
thread1.start()
thread2.start()
