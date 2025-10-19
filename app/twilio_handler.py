from fastapi import APIRouter, Form, Response
from twilio.twiml.voice_response import VoiceResponse
import requests
import tempfile
import os
from dotenv import load_dotenv

# ✅ Load environment variables first
load_dotenv()

# ✅ Correct way to get API key from .env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("⚠️ Missing GEMINI_API_KEY in .env file!")

# ✅ Import other modules *after* loading env
from app.utils.stt_tts import transcribe_audio
from app.database import save_conversation
from google import genai
from app.utils.rag_faq import get_faq_response

# ✅ Initialize Gemini client using the key
client = genai.Client(api_key=GEMINI_API_KEY)

# ✅ Initialize FastAPI router
router = APIRouter()

LANG_MAPPING = {
    "en": "Polly.Joanna",  # English female voice
    "ur": "Polly.Aditi"    # Closest to Urdu/Hindi
}

@router.post("/twilio/voice")
async def voice_webhook(
    CallSid: str = Form(...),
    From: str = Form(...),
    RecordingUrl: str = Form(None),
    lang: str = Form("en")
):
    """Handle incoming Twilio calls and respond using Gemini AI."""
    resp = VoiceResponse()

    # Step 1️⃣: First prompt
    if not RecordingUrl:
        resp.say("Hello! This is your AI assistant. Please speak after the beep.",
                 voice=LANG_MAPPING.get(lang, "Polly.Joanna"))
        resp.record(play_beep=True, max_length=10, action="/twilio/voice")
        return Response(content=str(resp), media_type="application/xml")

    # Step 2️⃣: Fetch recording
    try:
        audio_url = f"{RecordingUrl}.wav"
        audio_data = requests.get(audio_url).content
    except Exception as e:
        resp.say("Sorry, I could not retrieve your audio.")
        print(f"❌ Error fetching audio: {e}")
        return Response(content=str(resp), media_type="application/xml")

    # Step 3️⃣: Transcribe
    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            f.write(audio_data)
            user_text = transcribe_audio(f.name)
    except Exception as e:
        resp.say("Sorry, I could not understand that. Please try again.")
        print(f"❌ Transcription error: {e}")
        return Response(content=str(resp), media_type="application/xml")

    # Step 4️⃣: Check FAQ
    faq_reply = get_faq_response(user_text)

    # Step 5️⃣: Generate Gemini reply
    prompt = faq_reply if faq_reply else f"Reply in {lang}: {user_text}"
    try:
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        ai_reply = response.text.strip()
    except Exception as e:
        ai_reply = "Sorry, something went wrong with the AI response."
        print(f"❌ Gemini error: {e}")

    # Step 6️⃣: Respond via Twilio
    resp.say(ai_reply, voice=LANG_MAPPING.get(lang, "Polly.Joanna"))
    resp.record(play_beep=True, max_length=10, action="/twilio/voice")

    # Step 7️⃣: Save conversation
    try:
        save_conversation(user_text, ai_reply, lang)
    except Exception as e:
        print(f"⚠️ Database save error: {e}")

    print(f"📞 Caller {From} said: {user_text}")
    print(f"🤖 AI replied: {ai_reply}")

    return Response(content=str(resp), media_type="application/xml")
