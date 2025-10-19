import whisper
import pyttsx3
import numpy as np
from scipy.io.wavfile import write
import tempfile
import os

model = whisper.load_model("base")
engine = pyttsx3.init()
engine.setProperty("rate", 175)
engine.setProperty("volume", 1.0)

def transcribe_audio(audio_input, fs=16000):
    """Accepts either .wav file path or NumPy array"""
    if isinstance(audio_input, str) and os.path.exists(audio_input):
        result = model.transcribe(audio_input)
        return result["text"]
    elif isinstance(audio_input, np.ndarray):
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            write(f.name, fs, (audio_input * 32767).astype(np.int16))
            result = model.transcribe(f.name)
        return result["text"]
    else:
        raise ValueError("Invalid audio input")

def speak_text(text):
    engine.say(text)
    engine.runAndWait()
