import pyaudio
import numpy as np
import wave
import time
import ffmpeg

# Audio settings
FORMAT = pyaudio.paInt16  # 16-bit audio format
CHANNELS = 1  # Mono
RATE = 44100  # Sample rate (Hz)
CHUNK = 1024  # Buffer size
SILENCE_THRESHOLD = 500  # Adjust this value based on your environment
SILENCE_DURATION = 3  # Stop recording after this many seconds of silence
FILE_WAV_NAME = "./temp/recorded_audio.wav"
FILE_MP3_NAME = "./temp/recorded_audio.mp3"

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Start recording
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

print("Recording... Speak into the microphone.")

frames = []
silent_chunks = 0
start_time = time.time()

while True:
    data = stream.read(CHUNK)
    frames.append(data)

    # Convert audio data to numpy array
    audio_data = np.frombuffer(data, dtype=np.int16)
    volume = np.max(np.abs(audio_data))  # Get the max volume level in chunk

    if volume < SILENCE_THRESHOLD:
        silent_chunks += 1
    else:
        silent_chunks = 0  # Reset if sound is detected

    if silent_chunks > (SILENCE_DURATION * RATE / CHUNK):  # Convert seconds to chunks
        print("Silence detected. Stopping recording.")
        break

# Stop & close the stream
stream.stop_stream()
stream.close()
audio.terminate()

# Save the recorded audio
wave_file = wave.open(FILE_WAV_NAME, "wb")
wave_file.setnchannels(CHANNELS)
wave_file.setsampwidth(audio.get_sample_size(FORMAT))
wave_file.setframerate(RATE)
wave_file.writeframes(b''.join(frames))
wave_file.close()

print("Recording saved as 'recorded_audio.wav'.")

# Convert to MP3
ffmpeg.input(FILE_WAV_NAME).output(FILE_MP3_NAME, format='mp3', audio_bitrate="192k").run(overwrite_output=True)

print("Recording converted to mp3 as 'recorded_audio.mp3'.")
