def get_voice_params(emotion: str, intensity: float) -> dict:
    """
    Maps an emotion and its intensity to specific text-to-speech parameters.
    
    Args:
        emotion (str): The detected emotion (Happy, Neutral, Frustrated)
        intensity (float): The intensity of the emotion (0.0 to 1.0)
        
    Returns:
        dict: Target adjustments for pitch, rate, and volume.
        Pitch and Rate shifts are relative (e.g., +20 or -15 wpm/steps)
        Volume is absolute or relative delta.
        For ElevenLabs, these map broadly to stability and similarity parameters.
    """
    params = {
        "emotion": emotion,
        "pitch_shift": 0,    # Relative pitch shift (not natively robust in default pyttsx3, but implemented via hacks or ElevenLabs)
        "rate_shift": 0,     # Relative rate shift in words per minute (WPM delta)
        "volume_shift": 0.0, # Relative volume shift (-1.0 to 1.0 delta)
        "cloud_stability": 0.5, # ElevenLabs specific params
        "cloud_similarity": 0.5 
    }
    
    # Base multiplier to make effects more pronounced as intensity increases
    # We add 0.5 to baseline intensity to ensure even mild emotions have some effect
    scale = intensity + 0.5 if intensity > 0 else 0
    
    if emotion == "Happy":
        # Happy -> Higher pitch, faster rate, slightly louder
        params["rate_shift"] = int(50 * scale)        # up to +75 wpm faster
        params["volume_shift"] = min(0.3 * scale, 1.0) # Up to +0.3 louder
        params["cloud_stability"] = 0.3               # More expressive
        params["cloud_similarity"] = 0.8
        
    elif emotion == "Frustrated":
        # Frustrated/Sad -> Lower pitch, slower rate, softer tone OR louder if very intense
        if intensity > 0.6:
            # Angry/Very Frustrated
            params["rate_shift"] = int(20 * scale)
            params["volume_shift"] = min(0.4 * scale, 1.0)
            params["cloud_stability"] = 0.2
        else:
            # Sad/Mildly Frustrated
            params["rate_shift"] = int(-40 * scale)   # up to -60 wpm slower
            params["volume_shift"] = -0.2 * scale     # slightly softer
            params["cloud_stability"] = 0.7
            
    # Neutral retains baseline 0 mappings
    return params
