import os
import time
import pyttsx3
import traceback
from elevenlabs import generate, set_api_key, save
from app.utils import setup_logger

logger = setup_logger("tts_engine")
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

try:
    import pythoncom
    WINDOWS_MODE = True
except ImportError:
    WINDOWS_MODE = False

def generate_local_audio(text: str, params: dict) -> str:
    """
    Uses pyttsx3 to generate local TTS audio and saves it as .wav
    """
    logger.info("Initializing pyttsx3 (local) generation")
    if WINDOWS_MODE:
        pythoncom.CoInitialize()
        
    engine = pyttsx3.init()
    
    # Adjust Rate
    base_rate = engine.getProperty('rate')
    target_rate = max(50, base_rate + params.get('rate_shift', 0))
    engine.setProperty('rate', target_rate)
    
    # Adjust Volume
    base_volume = engine.getProperty('volume')
    target_volume = base_volume + params.get('volume_shift', 0)
    target_volume = min(max(target_volume, 0.1), 1.0)
    engine.setProperty('volume', target_volume)
    
    timestamp = int(time.time())
    output_path = os.path.join(OUTPUT_DIR, f"speech_{timestamp}.wav")
    
    engine.save_to_file(text, output_path)
    engine.runAndWait()
    
    if WINDOWS_MODE:
        pythoncom.CoUninitialize()
        
    logger.info(f"Successfully generated local audio -> {output_path}")
    return output_path

def generate_cloud_audio(text: str, emotion: str) -> str:
    """
    Uses ElevenLabs API directly via "from elevenlabs import generate" 
    to create an expressive cloud TTS output.
    """
    api_key = os.getenv("ELEVENLABS_API_KEY", "")
    if not api_key:
        raise ValueError("Cannot access ElevenLabs without an API key.")
        
    set_api_key(api_key)
    logger.info("Initializing ElevenLabs generation")
    
    # 🎭 Modify logic to reflect emotion
    processed_text = text
    if emotion == "Happy":
        # Example formatting for energetic, faster pacing
        processed_text = processed_text.replace(".", "!").replace(",", "!")
    elif emotion == "Frustrated" or emotion == "Negative":
        # Slower pacing - insert pauses
        processed_text = processed_text.replace(" ", " ... ")
    elif emotion == "Neutral":
        pass # keep balanced tone

    try:
        audio = generate(
            text=processed_text,
            voice="Rachel",
            model="eleven_multilingual_v2"
        )
        # Using specific output path requested
        output_path = os.path.join(OUTPUT_DIR, "output.mp3")
        save(audio, output_path)
        logger.info(f"Successfully generated cloud audio -> {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"ElevenLabs failed: {e}. Raising error to trigger fallback.")
        raise
