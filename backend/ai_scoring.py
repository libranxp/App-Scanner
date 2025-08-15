import numpy as np

def ai_score(data_point):
    """
    AI scoring function:
    - momentum: 50% weight
    - sentiment_score: 30% weight
    - relative_volume: 20% weight
    """
    momentum = data_point.get("momentum", 0)
    sentiment = data_point.get("sentiment_score", 0)
    rel_vol = data_point.get("relative_volume", 0)
    score = 0.5 * momentum + 0.3 * sentiment + 0.2 * rel_vol
    return round(score, 2)
