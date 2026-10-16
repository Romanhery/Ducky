import sounddevice as sd
from scipy.io.wavfile import write

SAMPLE_RATE = 44100   # Hz
DURATION = 10         # seconds
FILENAME = "recording.mp3"

print(f"Recording for {DURATION} seconds...")
audio = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype="int16")
sd.wait()  # block until recording finishes

write(FILENAME, SAMPLE_RATE, audio)
print(f"Saved to {FILENAME}")