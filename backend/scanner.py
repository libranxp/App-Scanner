# backend/scanner.py
import json
import os
from backend.sentiment import analyze_sentiment
from backend.telegram import send_telegram_message

SIGNALS_FILE = "signals.json"

def fetch_stocks():
    # Replace with API calls using your keys (FMP, Polygon, Finnhub, etc.)
    # Returns list of dicts: {"ticker": "AAPL", "news": "Apple earnings report positive"}
    return []

def fetch_crypto():
    # Replace with API calls using your keys (CoinGecko, CoinMarketCal, LunarCrush)
    return []

def process_assets(assets, asset_type="stock"):
    signals = []
    for asset in assets:
        text = asset.get("news", "")
        score = analyze_sentiment(text)
        if score != 0:
            signals.append({"symbol": asset.get("ticker"), "score": score, "news": text})
            send_telegram_message(f"{asset.get('ticker')}: {text}", channel=asset_type)
    return signals

def main():
    stocks = fetch_stocks()
    crypto = fetch_crypto()

    stock_signals = process_assets(stocks, "stock")
    crypto_signals = process_assets(crypto, "crypto")

    all_signals = {"stocks": stock_signals, "crypto": crypto_signals}

    with open(SIGNALS_FILE, "w") as f:
        json.dump(all_signals, f, indent=2)
    print("Signals updated.")

if __name__ == "__main__":
    main()
