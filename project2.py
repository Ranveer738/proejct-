import sounddevice as sd
import matplotlib.pyplot as plt
import numpy as np
import speech_recognition as sr
import wave

rate = 16000

print("Recording started... Press Enter to stop.")
recording = []

def callback(indata, frames, time, status):
    recording.append(indata.copy())

stream = sd.InputStream(samplerate=rate, channels=1, callback=callback)
with stream:
    input()

print("Recording stopped. Processing audio...")

audio_Data = np.concatenate(recording, axis=0).flatten()
audio_bytes = (audio_Data * 32767).astype(np.int16).tobytes()

with wave.open("speech.wav", "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(rate)
    wf.writeframes(audio_bytes)
print("Saved raw audio to speech.wav")

recognizer = sr.Recognizer()
try:
    audio_obj = sr.AudioData(audio_bytes, rate, 2)
    text = recognizer.recognize_google(audio_obj)
except Exception:
    text = "[Could not transcribe]"

print(f"Transcription: {text}")
with open("speech.txt", "w") as f:
    f.write(text)
print("Saved transcription to speech.txt")

plt.figure(figsize=(10, 4))
plt.plot(audio_Data, color="blue")
plt.title("Audio Waveform")
plt.xlabel("Samples")
plt.ylabel("Amplitude")
plt.tight_layout()
plt.show()