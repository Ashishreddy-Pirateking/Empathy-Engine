import argparse
import sys
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv

import app.emotion as emotion
import app.voice_mapper as voice_mapper

from api.routes import router

load_dotenv()

# Setup FastAPI App
app = FastAPI(
    title="The Empathy Engine",
    description="Detects emotional tone from text and generates expressive speech by modifying audio parameters.",
    version="1.0.0"
)

# API Routes
app.include_router(router, prefix="/api")

# Serve the generated audio files statically
app.mount("/audio", StaticFiles(directory="outputs"), name="outputs")

# Serve the frontend
@app.get("/")
def read_index():
    return FileResponse("ui/index.html")

def cli_mode(text: str):
    """
    Executes the empathetic synthesis pipeline directly from the command line.
    """
    print(f"\n[CLI Mode] Processing text: '{text}'")
    
    # 1. Detect emotion
    res = emotion.detect_emotion(text)
    print(f"-> Emotion: {res['emotion']} (Intensity: {res['intensity']:.2f})")
    
    # 2. Get params
    params = voice_mapper.get_voice_params(res['emotion'], res['intensity'])
    print(f"-> TTS Params Mapped: {params}")
    
    # 3. Generate Audio
    import os
    mode = os.getenv("TTS_MODE", "local")
    api_key_exists = bool(os.getenv("ELEVENLABS_API_KEY", "").strip())
    
    if mode == "cloud" and api_key_exists:
        try:
            from app.tts_engine import generate_cloud_audio
            out_path = generate_cloud_audio(text, res['emotion'])
            print(f"-> Mode: Cloud (ElevenLabs)")
        except Exception as e:
            print(f"-> Cloud failed: {e}. Falling back to local.")
            from app.tts_engine import generate_local_audio
            out_path = generate_local_audio(text, params)
            print(f"-> Mode: Local Fallback (pyttsx3)")
    else:
        from app.tts_engine import generate_local_audio
        out_path = generate_local_audio(text, params)
        print(f"-> Mode: Local (pyttsx3)")
        
    print(f"-> Output saved to: {out_path}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="The Empathy Engine - Voice Synthesis")
    parser.add_argument("--text", type=str, help="Text to synthesize immediately via CLI")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the API server on")
    
    args = parser.parse_args()
    
    if args.text:
        cli_mode(args.text)
    else:
        # Run Web Server
        print("Starting FastAPI Server...")
        uvicorn.run("app.main:app", host="0.0.0.0", port=args.port, reload=True)
