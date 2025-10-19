# phase2
# In main.py or a separate utils file
import pyttsx3
from tempfile import NamedTemporaryFile

engine = pyttsx3.init()
engine.setProperty("rate", 175)
engine.setProperty("volume", 1.0)

def text_to_speech(text):
    """Convert text to speech and return WAV file path"""
    with NamedTemporaryFile(suffix=".wav", delete=False) as f:
        engine.save_to_file(text, f.name)
        engine.runAndWait()
        return f.name
