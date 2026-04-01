from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import asyncio
from typing import Dict, Any

from app.emotion import detect_emotion
from app.voice_mapper import get_voice_params

from app.utils import setup_logger

logger = setup_logger("routes")
router = APIRouter()

class SynthesizeRequest(BaseModel):
    text: str

class SynthesizeResponse(BaseModel):
    emotion: str
    intensity: float
    audio_path: str
    parameters_used: Dict[str, Any]
    mode: str

@router.post("/synthesize", response_model=SynthesizeResponse)
async def synthesize_speech(request: SynthesizeRequest):
    """
    Main endpoint that accepts text, processes emotion, formats TTS config, 
    generates audio, and returns data and audio path.
    """
    text = request.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty.")
    
    logger.info(f"Received synthesize request: {text[:50]}...")
    
    # 1. Detect Emotion
    emotion_result = detect_emotion(text)
    emotion = emotion_result['emotion']
    intensity = emotion_result['intensity']
    
    # 2. Map Voice Parameters (used for local)
    voice_params = get_voice_params(emotion, intensity)
    
    # 3. Read Mode configuration
    mode_pref = os.getenv("TTS_MODE", "local")
    api_key_exists = bool(os.getenv("ELEVENLABS_API_KEY", "").strip())
    
    # 4. Generate Audio (offloaded to thread since pyttsx3 is blocking/elevenlabs makes requests)
    audio_path = ""
    used_mode = mode_pref
    
    if mode_pref == "cloud" and api_key_exists:
        try:
            from app.tts_engine import generate_cloud_audio
            audio_path = await asyncio.to_thread(generate_cloud_audio, text, emotion)
            used_mode = "cloud"
        except Exception as e:
            logger.error(f"Cloud TTS failed, falling back to local: {e}")
            from app.tts_engine import generate_local_audio
            audio_path = await asyncio.to_thread(generate_local_audio, text, voice_params)
            used_mode = "local"
    else:
        from app.tts_engine import generate_local_audio
        audio_path = await asyncio.to_thread(generate_local_audio, text, voice_params)
        used_mode = "local"
        
    return SynthesizeResponse(
        emotion=emotion,
        intensity=intensity,
        audio_path=audio_path,
        parameters_used=voice_params,
        mode=used_mode
    )
