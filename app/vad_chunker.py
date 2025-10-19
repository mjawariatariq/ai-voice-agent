# Phase 1 – Core AI Bricks

# 🎯 Goal: Speech pipeline ready (STT → NLP → TTS)

# STT (Speech-to-Text):  Whisper / Google STT API integrate karo. Audio input lo, text return karo.

# NLP / Brain: GPT API (start simple with OpenAI).

# Later: Add RAG with FAISS / Pinecone (store FAQs, docs).

# TTS (Text-to-Speech): Start simple: pyttsx3 or Edge TTS.

#Later: upgrade to ElevenLabs/Azure TTS.

#Test: Mic se bolo → Text → GPT response → Voice reply.

#####vad_chunker.py

# STT (Speech-to-Text):

import sounddevice as sd
import numpy as np
import tempfile
from scipy.io.wavfile import write
import whisper
import pyttsx3
from google import genai  # ✅ Gemini client

# Initialize Gemini client (use your Gemini API key)
client = genai.Client(api_key="AIzaSyC9OAVmSvQ1AWcTLtyLdxuVAER8uScCEqE")


# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 175)  # Speed of speech
engine.setProperty("volume", 1.0) # Volume (0.0 to 1.0)

# Load Whisper model (local)
model = whisper.load_model("base")  # can use "small" or "medium" for better accuracy

def record_audio(duration=5, fs=16000):
    print("🎙️ Speak now...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()
    print("✅ Recording complete.")
    return audio
sd.wait()

def transcribe_audio(audio, fs=16000):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        write(f.name, fs, (audio * 32767).astype(np.int16))
        result = model.transcribe(f.name)
    return result['text']

def speak_text(text):
    print("🗣️ Speaking...")
    engine.say(text)
    engine.runAndWait()

# 🎧 Main loop
while True:
    audio = record_audio(duration=5)
    text = transcribe_audio(audio)
    print("🗣️ You said:", text)

    if text.strip().lower() in ["exit", "quit", "stop"]:
        print("👋 Exiting...")
        speak_text("Goodbye! See you soon.")
        break
 
    # ✨ Gemini Response
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=text
    )

    reply = response.text
    print("🤖 AI says:", reply)
    speak_text(reply)
