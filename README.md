sounddevice → Access your microphone to record audio.
numpy → For audio array manipulation. The recorded audio comes as a NumPy array.
tempfile → Creates temporary files in your system. We use this to save audio chunks before sending them to OpenAI.
scipy.io.wavfile.write → Converts the NumPy array into a WAV file, which Whisper API can read.
openai.OpenAI → The client object to call OpenAI APIs, in this case, Whisper transcription.

