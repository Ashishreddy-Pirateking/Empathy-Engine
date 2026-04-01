from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from app.utils import setup_logger

logger = setup_logger("emotion")
analyzer = SentimentIntensityAnalyzer()

def detect_emotion(text: str) -> dict:
    """
    Analyzes the sentiment of precisely given text.
    Classifies into 3 categories: Happy, Neutral, Frustrated.
    Also returns an intensity metric.
    
    Args:
        text (str): The input text to analyze.
        
    Returns:
        dict: A dictionary containing 'emotion' and 'intensity'.
    """
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']
    
    # Calculate intensity on a 0.0 to 1.0 scale (absolute value of compound score)
    # Neutral text gets an intensity of 0.0
    intensity = abs(compound)
    
    if compound >= 0.05:
        emotion = "Happy"
    elif compound <= -0.05:
        emotion = "Frustrated"
    else:
        emotion = "Neutral"
        
    logger.info(f"Detected Emotion: {emotion} | Intensity: {intensity:.2f} | Score: {compound}")
    
    return {
        "emotion": emotion,
        "intensity": intensity
    }
