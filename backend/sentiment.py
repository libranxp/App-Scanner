# backend/sentiment.py
import requests

def analyze_sentiment(text):
    """
    Analyzes sentiment of given text using a simple API or local logic.
    Replace this with any external API if you have keys, e.g., OpenAI, etc.
    """
    text = text.lower()
    score = 0
    if any(word in text for word in ["good", "up", "positive", "buy"]):
        score += 1
    if any(word in text for word in ["bad", "down", "negative", "sell"]):
        score -= 1
    return score
