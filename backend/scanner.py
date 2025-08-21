import time
from backend.providers import (
    alphavantage, coinglass, coinmarketcal, finnhub, fmp,
    lunarcrush, messari, newsapi, polygon, reddit, santiment, twitter
)
from utils.util import save_json, get_timestamp
from utils.risk import calculate_risk
from ai_scoring import compute_ai_score

# Define your scan criteria
CRYPTO_CRITERIA = {
    "price_min": 0.001,
    "price_max": 100,
    "volume_min": 10_000_000,
    "change_min": 2,
    "change_max": 20,
    "market_cap_min": 10_000_000,
    "market_cap_max": 5_000_000_000,
    "rsi_min": 50,
    "rsi_max": 70,
    "rvol_min": 2,
    "ema_alignment": True,
    "vwap_proximity": 0.02,
    "duplicate_window": 6,
    "twitter_mentions_min": 10,
    "engagement_min": 100,
    "sentiment_min": 0.6
}

STOCK_CRITERIA = {
    "price_min": 0.04,
    "volume_min": 500_000,
    "change_min": 1,
    "rvol_min": 1.2,
    "rsi_min": 45,
    "rsi_max": 75,
    "ema_alignment": True,
    "vwap_proximity": 0.015,
    "twitter_buzz_min": 5,
    "engagement_min": 50,
    "sentiment_min": 0.6
}

def run_tier1_scan():
    timestamp = get_timestamp()
    crypto_results = []
    stock_results = []

    # Dynamically fetch tickers from providers
    crypto_tickers = coinglass.get_active_tickers()
    stock_tickers = polygon.get_active_tickers()

    for ticker in crypto_tickers:
        try:
            data = finnhub.get_crypto_data(ticker)
            if not meets_criteria(data, CRYPTO_CRITERIA):
                continue
            enriched = enrich_asset(ticker, data, asset_type="crypto")
            crypto_results.append(enriched)
        except Exception as e:
            crypto_results.append({"ticker": ticker, "error": str(e)})

    for ticker in stock_tickers:
        try:
            data = fmp.get_stock_data(ticker)
            if not meets_criteria(data, STOCK_CRITERIA):
                continue
            enriched = enrich_asset(ticker, data, asset_type="stock")
            stock_results.append(enriched)
        except Exception as e:
            stock_results.append({"ticker": ticker, "error": str(e)})

    save_json("data/latest_crypto.json", crypto_results)
    save_json("data/latest_stocks.json", stock_results)
    return crypto_results + stock_results

def meets_criteria(data, criteria):
    # Apply filters based on asset type
    try:
        if not (criteria["price_min"] <= data["price"] <= criteria["price_max"]):
            return False
        if data["volume"] < criteria["volume_min"]:
            return False
        if "change_min" in criteria and data["change"] < criteria["change_min"]:
            return False
        if "rsi_min" in criteria and data["rsi"] < criteria["rsi_min"]:
            return False
        if "rvol_min" in criteria and data["rvol"] < criteria["rvol_min"]:
            return False
        # Add more filters as needed
        return True
    except:
        return False

def enrich_asset(ticker, data, asset_type="crypto"):
    sentiment = sentiment_score(ticker)
    catalyst = catalyst_summary(ticker)
    ai_score, confidence, narrative = compute_ai_score(data, sentiment, catalyst)
    risk = calculate_risk(data)

    return {
        "ticker": ticker,
        "price": data["price"],
        "change": data["change"],
        "volume": data["volume"],
        "rsi": data["rsi"],
        "ema": data["ema"],
        "vwap": data["vwap"],
        "rvol": data["rvol"],
        "ai_score": ai_score,
        "confidence": confidence,
        "narrative": narrative,
        "risk": risk,
        "sentiment": sentiment,
        "catalyst": catalyst,
        "asset_type": asset_type,
        "timestamp": get_timestamp()
    }

def sentiment_score(ticker):
    return {
        "score": lunarcrush.get_sentiment(ticker),
        "twitter": twitter.get_mentions(ticker),
        "reddit": reddit.get_sentiment(ticker),
        "news": newsapi.get_sentiment(ticker)
    }

def catalyst_summary(ticker):
    return {
        "tweet": twitter.get_top_tweet(ticker),
        "headline": newsapi.get_top_headline(ticker),
        "reddit": reddit.get_top_thread(ticker),
        "calendar": coinmarketcal.get_event(ticker)
    }
