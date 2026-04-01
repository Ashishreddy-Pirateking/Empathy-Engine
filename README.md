# The Empathy Engine
Giving AI a Human Voice

The Empathy Engine is a complete system that processes textual input, detects its emotional tone (Happy, Neutral, or Frustrated), and dynamically modifies text-to-speech (TTS) parameters (such as pitch, rate, and volume) to match that emotion.

## Features
- **Emotion Detection**: Utilizes `vaderSentiment` to analyze input text.
- **Dynamic Voice Mapping**: Scales text-to-speech variables using the detected emotional intensity.
  - Positive/Happy -> Faster rate, slightly louder.
  - Negative/Frustrated -> Slower rate, softer tone (or loud if incredibly angry).
- **Dual Interfaces**: Access the engine via the sleek web UI or directly through the CLI.
- **Cloud & Local TTS**: Uses `pyttsx3` locally by default, but seamlessly supports ElevenLabs by changing `.env`.

## Hybrid TTS System
This project supports dual-engine functionality controlled completely via your `.env` file (`TTS_MODE` flag):
- **ElevenLabs (Cloud)**: Produces highly expressive speech. Set `TTS_MODE=cloud` and configure your `ELEVENLABS_API_KEY` to enable. Emotion intensity modifies phrasing (e.g. pauses for frustrated tone or speedy exclamation injections for happy tones).
- **Pyttsx3 (Local)**: A robotic, 100% offline baseline fallback mechanism. Modifies system parameters mapping intensity numerically. Automatically gracefully falls back if the cloud API fails.

## Architecture

```
empathy-engine/
│── app/
│   ├── main.py             # FastAPI initialization, routing attachment, CLI logic
│   ├── emotion.py          # vaderSentiment analysis generating compound intensity metrics
│   ├── voice_mapper.py     # Converts NLP output into TTS mechanical parameters
│   ├── tts_engine.py       # Interacts with System OS to generate WAV
│   ├── utils.py            # Global logging handler
│
│── api/
│   ├── routes.py           # Exposes /api/synthesize
│
│── ui/
│   ├── index.html          # Modern, dynamic aesthetic web UI with Fetch API caller
│
│── outputs/                # Ignored cache directory where generated chunks live
│── requirements.txt        
│── .env                    
```

### Emotion-to-Voice Mapping Logic
- **Detection**: VADER returns a "compound score" (-1.0 to 1.0).
- **Intensity Mapping**: The absolute value determines how intensely the emotion scales parameters.
- **Conversion** (`app/voice_mapper.py`):
    - **Happy** (`compound > 0.05`): Increases words-per-minute (`WPM`) up to +75 based on scale. Increases pyttsx3 volume by up to +0.3.
    - **Frustrated** (`compound < -0.05`):
        - Mildly sad (`intensity < 0.6`): Slows down WPM substantially (-60). Decreases volume.
        - Outwardly angry (`intensity >= 0.6`): Increases speed and volume.

## Setup Instructions

1. **Clone & Setup Environment**
   Ensure Python 3.9+ is installed.
   ```bash
   cd empathy-engine
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On MacOS/Linux:
   # source venv/bin/activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Setup**
   A `.env` file is generated. Ensure `TTS_MODE=local` to run strictly local Pyttsx3.
   To run ElevenLabs, change it to `TTS_MODE=cloud` and provide an API key.

## Executing the Application

### 1. Web UI & API Server (Recommended)
Run the following command starting from the `empathy-engine` root directory:
```bash
python -m app.main
```
Then visit: `http://localhost:8000`

### 2. CLI Mode (Headless)
Run a quick synthesis without starting the server:
```bash
python -m app.main --text "I am feeling so incredibly fantastic today!"
```
The output file path and applied parameters will be printed in the terminal.

## Example Inputs
- *"I am having the greatest day of my entire life, everything is perfect!"* (Outputs Happy, max intensity, fast rate)
- *"I ordered my food two hours ago and you guys still haven't delivered it. This is completely unacceptable!"* (Outputs Frustrated, loud volume, fast rate for anger)
- *"The package has arrived at the facility."* (Outputs Neutral, flat profile)
