from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.twilio_handler import router as twilio_router

app = FastAPI(title="AI Voice Agent")

# Mount static folder (for frontend files)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include Twilio router
app.include_router(twilio_router)

@app.get("/health")
def health():
    return {"status": "✅ AI Voice Agent running properly"}

from fastapi import FastAPI
from app.twilio_handler import router as twilio_router

app = FastAPI()

# ✅ Add this root route
@app.get("/")
def home():
    return {"message": "AI Voice Agent backend is running ✅"}

# Mount the Twilio routes
app.include_router(twilio_router)
