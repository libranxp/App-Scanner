# backend/sentiment.py
# Live, provider-backed sentiment scoring with no pre-picked tickers or sample data.

import math
from typing import List, Dict

# Use your existing provider modules (which read API keys from env/secrets)
from backend.providers import twitter, newsapi


# --- Simple lexicon for lightweight polarity (you can expand these safely) ---
_POS_WORDS = {
    "beat", "breakout", "bull", "bullish", "buy", "green", "growth", "high", "surge",
    "rally", "moon", "rocket", "pop", "up", "upgrade", "strong", "positive", "win",
    "gain", "soar", "spike"
}
_NEG_WORDS = {
    "miss", "bear", "bearish", "sell", "red", "drop", "down", "downgrade", "weak",
    "negative", "loss", "dump", "plunge", "halt", "ban", "warning", "crash", "risk"
}


def _polarity_score(text: str) -> float:
    """
    Very lightweight polarity estimator: (#pos - #neg) / tokens (clipped).
    This avoids any pre-trained models and works entirely on GitHub Actions.
    """
    if not text:
        return 0.0
    tokens = text.lower().split()
    if not tokens:
        return 0.0

    pos = sum(1 for t in tokens if t in _POS_WORDS)
    neg = sum(1 for t in tokens if t in _NEG_WORDS)
    raw = (pos - neg) / max(len(tokens), 1)

    # clip to a small band, then squash with sigmoid to [0,1]
    raw = max(min(raw, 0.2), -0.2)
    return 1.0 / (1.0 + math.exp(-20.0 * raw))  # steep sigmoid around 0


def _collect_texts(symbol: str, asset_type: str) -> List[str]:
    """
    Pulls recent tweets and related news titles/descriptions for the symbol.
    Uses only live data via your provider wrappers.
    """
    query = f"({symbol} OR ${symbol}) lang:en -is:retweet"
    tweets = []
    try:
        tweets = twitter.fetch_tweets(query=query, max_results=50) or []
    except Exception:
        tweets = []

    articles = []
    try:
        articles = newsapi.fetch_news(query=symbol) or []
    except Exception:
        articles = []

    texts: List[str] = []
    for t in tweets:
        txt = t.get("text") or ""
        if txt:
            texts.append(txt)
    for a in articles:
        title = a.get("title") or ""
        desc = a.get("description") or ""
        combined = f"{title} {desc}".strip()
        if combined:
            texts.append(combined)

    return texts


def sentiment_score(symbol: str, asset_type: str = "stock") -> float:
    """
    Public API used by scanner.py
    Returns a normalized sentiment score in [0.0, 1.0], computed from live tweets & news.
    If no data is available, returns 0.5 (neutral).
    """
    texts = _collect_texts(symbol, asset_type)
    if not texts:
        return 0.5  # neutral when data is sparse/unavailable

    # average polarity across texts
    scores = [_polarity_score(t) for t in texts]
    avg = sum(scores) / max(len(scores), 1)
    # bound and round to 2 decimals for stable UI/filters
    return round(max(0.0, min(1.0, avg)), 2)


def sentiment_links(symbol: str) -> Dict[str, str]:
    """
    Optional helper: direct links you can embed in alerts/UI if needed.
    Your scanner can ignore this if it already builds links elsewhere.
    """
    return {
        "twitter": f"https://twitter.com/search?q=%24{symbol}%20OR%20{symbol}&src=typed_query&f=live",
        "news": f"https://news.google.com/search?q={symbol}",
        "reddit": f"https://www.reddit.com/search/?q={symbol}",
    }
