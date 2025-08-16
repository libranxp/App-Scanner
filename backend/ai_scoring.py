# backend/ai_scoring.py
def calculate_ai_score(ticker, price, change_pct, sentiment, catalysts):
    """
    Returns AI score from 1–10 based on price movement and sentiment.
    """
    score = 5  # default neutral
    score += min(max(change_pct / 2, -5), 5)  # movement effect
    if sentiment > 0.5:
        score += 2
    elif sentiment < -0.5:
        score -= 2

    return max(1, min(10, round(score, 1)))


def generate_reason(ticker, price, change_pct, sentiment, catalysts):
    """
    Returns a concise explanation string for AI score.
    """
    reasons = []
    if change_pct > 2:
        reasons.append("Strong price movement")
    elif change_pct < -2:
        reasons.append("Weak price movement")

    if sentiment > 0.5:
        reasons.append("Positive social sentiment")
    elif sentiment < -0.5:
        reasons.append("Negative social sentiment")

    if catalysts:
        reasons.append("Upcoming catalyst event")

    return " | ".join(reasons) if reasons else "Neutral conditions"
