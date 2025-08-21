from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Placeholder model — replace with trained model if available
model = RandomForestClassifier()

def compute_ai_score(data, sentiment, catalyst):
    score = 0
    confidence = "Medium"
    narrative = ""

    # Feature weights (adjust as needed)
    weights = {
        "rsi": 0.1,
        "ema_alignment": 0.15,
        "vwap_proximity": 0.1,
        "rvol": 0.15,
        "volume": 0.1,
        "sentiment_score": 0.2,
        "catalyst_score": 0.2
    }

    # Normalize inputs
    rsi = normalize(data.get("rsi", 50), 0, 100)
    ema = 1 if data.get("ema", {}).get("alignment") else 0
    vwap = 1 - abs(data.get("vwap_proximity", 0))
    rvol = normalize(data.get("rvol", 1), 0, 5)
    volume = normalize(data.get("volume", 1_000_000), 0, 100_000_000)
    sentiment_score = normalize(sentiment.get("score", 0.5), 0, 1)
    catalyst_score = catalyst_strength(catalyst)

    # Weighted sum
    score += rsi * weights["rsi"]
    score += ema * weights["ema_alignment"]
    score += vwap * weights["vwap_proximity"]
    score += rvol * weights["rvol"]
    score += volume * weights["volume"]
    score += sentiment_score * weights["sentiment_score"]
    score += catalyst_score * weights["catalyst_score"]

    # Final score scaling
    ai_score = round(score * 10, 2)

    # Confidence level
    if ai_score >= 8:
        confidence = "High"
    elif ai_score >= 5:
        confidence = "Medium"
    else:
        confidence = "Low"

    # Narrative generation
    reasons = []
    if sentiment_score > 0.6:
        reasons.append("Strong sentiment")
    if catalyst_score > 0.5:
        reasons.append("Catalyst detected")
    if ema:
        reasons.append("EMA alignment")
    if rvol > 0.5:
        reasons.append("High RVOL")
    if vwap > 0.8:
        reasons.append("VWAP proximity")

    narrative = ", ".join(reasons) if reasons else "No strong signals"

    return ai_score, confidence, narrative

def normalize(value, min_val, max_val):
    return max(0, min(1, (value - min_val) / (max_val - min_val)))

def catalyst_strength(catalyst):
    score = 0
    if catalyst.get("tweet"):
        score += 0.3
    if catalyst.get("headline"):
        score += 0.3
    if catalyst.get("reddit"):
        score += 0.2
    if catalyst.get("calendar"):
        score += 0.2
    return min(score, 1.0)
