def enhance_text(text, emotion, intensity):
    text = text.strip()

    if emotion == "joy":
        return f"Haha! {text}!" if intensity > 0.5 else f"Heh, {text}"

    elif emotion == "excitement":
        return f"Wow! This is amazing! {text}!"

    elif emotion == "sarcasm":
        return f"Ohhh, suuure... {text}..."

    elif emotion == "compassion":
        return f"Hey, it's okay. {text}"

    elif emotion == "anger":
        return f"{text.upper()}!"

    elif emotion == "sadness":
        return f"...{text}..."

    return text