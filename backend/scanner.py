# backend/scanner.py
# Main scanner orchestration – no pre-picked tickers or sample data

import os
import json
from pathlib import Path
from backend.providers import finnhub, polygon, fmp
from backend.sentiment import sentiment_score
from backend.ai_scoring import ai_score
from backend.risk import risk_assessment
from backend.utils.telegram import send_telegram_message

TRIGGER_LOG_FILE = Path("trigger_log.json")


def load_trigger_log():
    """Load trigger log safely. If file is missing or invalid, return {}."""
    if not TRIGGER_LOG_FILE.exists():
        return {}
    try:
        with open(TRIGGER_LOG_FILE, "r") as f:
            data = f.read().strip()
            if not data:
                return {}
            return json.loads(data)
    except Exception:
        return {}


def save_trigger_log(log):
    """Save trigger log safely to disk."""
    with open(TRIGGER_LOG_FILE, "w") as f:
        json.dump(log, f, indent=2)


def build_alert(symbol: str, asset_type: str = "stock") -> dict:
    """Builds a full alert object for symbol from multiple providers."""
    try:
        # Fetch price (stock or crypto)
        if asset_type == "stock":
            data = finnhub.fetch_stock_data(symbol)
            price = float(data.get("c", 0))
        else:
            data = polygon.fetch_crypto_price(symbol)
            price = float(data.get("price", 0))
    except Exception:
        price = 0.0

    # Sentiment + AI + Risk
    senti = sentiment_score(symbol)
    ai = ai_score(symbol, asset_type=asset_type)
    risk = risk_assessment(symbol, asset_type=asset_type)

    return {
        "symbol": symbol,
        "asset_type": asset_type,
        "price": str(price),
        "sentiment": senti,
        "ai_score": ai,
        "risk": risk,
    }


def run_scan():
    """Main scan loop."""
    log = load_trigger_log()

    # Fetch dynamic tickers (no pre-picked values)
    stock_symbols = fmp.fetch_most_active()      # must be API-driven
    crypto_symbols = polygon.fetch_top_crypto()  # must be API-driven

    results = []

    for symbol in stock_symbols:
        alert = build_alert(symbol, "stock")
        results.append(alert)
        send_telegram_message(alert)

    for symbol in crypto_symbols:
        alert = build_alert(symbol, "crypto")
        results.append(alert)
        send_telegram_message(alert)

    # Save updated run log
    log["last_run"] = results
    save_trigger_log(log)

    # Save alerts for frontend
    with open("alerts.json", "w") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    run_scan()
