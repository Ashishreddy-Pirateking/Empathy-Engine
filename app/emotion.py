from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def detect_emotion(text):
    text_lower = text.lower()
    score = analyzer.polarity_scores(text)["compound"]

    if any(word in text_lower for word in ["haha", "lol", "lmao"]):
        return "joy", abs(score)

    if "!" in text_lower or "excited" in text_lower:
        return "excitement", abs(score)

    if any(word in text_lower for word in ["yeah right", "sure", "obviously"]):
        return "sarcasm", abs(score)

    if any(word in text_lower for word in ["sorry", "it's okay", "i understand"]):
        return "compassion", abs(score)

    if score > 0.5:
        return "joy", score
    elif score < -0.5:
        return "anger", abs(score)
    elif score < -0.2:
        return "sadness", abs(score)
    else:
        return "neutral", abs(score)