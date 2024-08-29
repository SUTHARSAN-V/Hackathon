import re

def preprocess_text(text):
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove unwanted characters and extra spaces
    text = re.sub(r'\s*\n\s*', ' ', text)
    text = text.strip()
    return text
