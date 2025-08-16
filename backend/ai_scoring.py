# backend/ai_scoring.py
# Lightweight AI-style scoring function with no pre-picked tickers or sample data.

import math
from typing import Dict

from backend.providers import twitter, newsapi
from backend.sentiment import sentiment_score


def _normalize(value: float, min_val: float, max_val: float) -> float:
    """Clamp and normalize a value to [0, 1]."""
    if max_val == min_val:
        return 0.0
    return max(0.0, min(1.0, (value - min_val) / (max_val - min_val)))


def ai_score(symbol: str, asset_type: str = "stock") -> float:
    """
    Computes a composite score for a symbol using:
    - sentiment (0–1)
    - recent tweet volume (scaled)
    - recent news article volume (scaled)

    Returns a float between 0.0 (weak) and 1.0 (strong).
    """
    # --- sentiment ---
    try:
        sent = sentiment_score(symbol, asset_type)
    except Exception:
        sent = 0.5

    # --- social signals ---
    try:
        tweets = twitter.fetch_tweets(query=f"({symbol} OR ${symbol}) lang:en -is:retweet", max_results=50) or []
        tweet_count = len(tweets)
    except Exception:
        tweet_count = 0

    try:
        articles = newsapi.fetch_news(query=symbol) or []
        news_count = len(articles)
    except Exception:
        news_count = 0

    # normalize counts (heuristics for scaling)
    tweet_factor = _normalize(tweet_count, 0, 100)  # cap at 100 tweets
    news_factor = _normalize(news_count, 0, 20)     # cap at 20 articles

    # weighted composite
    score = (0.6 * sent) + (0.25 * tweet_factor) + (0.15 * news_factor)

    return round(max(0.0, min(1.0, score)), 2)


def ai_explain(symbol: str, asset_type: str = "stock") -> Dict[str, float]:
    """
    Optional: returns the breakdown of the AI score for transparency.
    """
    try:
        sent = sentiment_score(symbol, asset_type)
    except Exception:
        sent = 0.5

    try:
        tweets = twitter.fetch_tweets(query=f"({symbol} OR ${symbol}) lang:en -is:retweet", max_results=50) or []
        tweet_count = len(tweets)
    except Exception:
        tweet_count = 0

    try:
        articles = newsapi.fetch_news(query=symbol) or []
        news_count = len(articles)
    except Exception:
        news_count = 0

    return {
        "sentiment": sent,
        "tweet_count": tweet_count,
        "news_count": news_count,
        "ai_score": ai_score(symbol, asset_type),
    }
