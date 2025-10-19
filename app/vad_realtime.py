# Phase 2 – Advanced Functionalities
# 🎯 Goal: Features jo aapne report mein likhe
# Add Realtime Response (Streaming) → WebSocket or Twilio Stream.
# Add VAD (Voice Activity Detection) → webrtcvad use karke silence detect karo.
# Add Super Low Latency → optimize audio chunking + async FastAPI.
# Add DB integration (Postgres/Mongo) → store user queries & logs.
# Add Customizability → config file ya admin panel (business apna FAQ upload kar sake).
# End test: Agent ab live voice conversation kar sake.

# # vad_realtime.py
import webrtcvad
import collections
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
import tempfile
import whisper
import pyttsx3
from google import genai
import os
from dotenv import load_dotenv
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# client = genai.Client(api_key="APIKEY")
model = whisper.load_model("base")

engine = pyttsx3.init()
engine.setProperty("rate", 175)
engine.setProperty("volume", 1.0)

vad = webrtcvad.Vad(2)  # 0–3 aggressiveness level
sample_rate = 16000
frame_duration = 30  # ms
frame_size = int(sample_rate * frame_duration / 1000)

def record_with_vad(max_duration=10):
    print("🎤 Speak when ready...")
    audio_buffer = []
    silence_frames = 0
    threshold = 15  # silence frames limit

    while True:
        frame = sd.rec(frame_size, samplerate=sample_rate, channels=1, dtype='float32')
        sd.wait()
        frame_bytes = (frame * 32767).astype(np.int16).tobytes()

        is_speech = vad.is_speech(frame_bytes, sample_rate)
        if is_speech:
            audio_buffer.append(frame)
            silence_frames = 0
        else:
            silence_frames += 1
            if silence_frames > threshold:
                break

        if len(audio_buffer) * frame_duration / 1000 > max_duration:
            break

    if not audio_buffer:
        print("⚠️ No speech detected.")
        return None

    audio = np.concatenate(audio_buffer)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        write(f.name, sample_rate, (audio * 32767).astype(np.int16))
        result = model.transcribe(f.name)
    return result['text']

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def run_realtime_agent():
    while True:
        text = record_with_vad()
        if not text:
            continue
        print("🗣️ You said:", text)
        if text.lower() in ["exit", "quit", "stop"]:
            speak_text("Goodbye!")
            break
        response = GEMINI_API_KEY.models.generate_content(model="gemini-2.0-flash", contents=text)
        reply = response.text
        print("🤖 AI:", reply)
        speak_text(reply)

if __name__ == "__main__":
    run_realtime_agent()
