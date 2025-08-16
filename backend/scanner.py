# backend/scanner.py
import os
import json
from datetime import datetime
from backend.telegram import send_telegram_message
from backend.providers import (
    finnhub, fmp, polygon, alphavantage, newsapi,
    lunarcrush, coinmarketcal, santiment, coinglass,
    messari, coingecko, reddit, twitter
)

DATA_DIR = "docs/data"
STOCK_FILE = os.path.join(DATA_DIR, "latest_stocks.json")
CRYPTO_FILE = os.path.join(DATA_DIR, "latest_crypto.json")
LOG_FILE = os.path.join(DATA_DIR, "trigger_log.json")

# Telegram Channels (from GitHub Secrets)
STOCK_CHANNEL = os.getenv("TELEGRAM_STOCK_CHANNEL_ID")
CRYPTO_CHANNEL = os.getenv("TELEGRAM_CRYPTO_CHANNEL_ID")

def log_trigger(event_type, message):
    """Append trigger logs to JSON file for frontend tracking"""
    log_entry = {
        "time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "event_type": event_type,
        "message": message
    }
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    else:
        logs = []

    logs.append(log_entry)

    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)


def save_data(file_path, data):
    """Save JSON data for frontend consumption"""
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)


def scan_stocks():
    """Fetch stock data from APIs and trigger alerts"""
    stock_alerts = []

    try:
        stocks = fmp.get_top_movers()  # example source
        news = newsapi.get_stock_news()
        sentiment_scores = finnhub.get_sentiment()

        for s in stocks:
            symbol = s.get("symbol")
            change = s.get("changePercent", 0)

            if abs(change) > 5:  # Alert condition
                msg = f"📈 Stock Alert: {symbol} moved {change:.2f}%"
                stock_alerts.append(msg)
                send_telegram_message(STOCK_CHANNEL, msg)
                log_trigger("stock", msg)

        save_data(STOCK_FILE, stocks)

    except Exception as e:
        print(f"[ERROR] Stock scan failed: {e}")

    return stock_alerts


def scan_crypto():
    """Fetch crypto data from APIs and trigger alerts"""
    crypto_alerts = []

    try:
        cryptos = coingecko.get_top_movers()
        lunar_data = lunarcrush.get_social_trends()
        events = coinmarketcal.get_upcoming_events()

        for c in cryptos:
            symbol = c.get("symbol")
            change = c.get("price_change_percentage_24h", 0)

            if abs(change) > 5:  # Alert condition
                msg = f"💎 Crypto Alert: {symbol.upper()} moved {change:.2f}%"
                crypto_alerts.append(msg)
                send_telegram_message(CRYPTO_CHANNEL, msg)
                log_trigger("crypto", msg)

        save_data(CRYPTO_FILE, cryptos)

    except Exception as e:
        print(f"[ERROR] Crypto scan failed: {e}")

    return crypto_alerts


def main():
    print("🔎 Running scanner...")

    stock_alerts = scan_stocks()
    crypto_alerts = scan_crypto()

    print(f"✅ Finished. Stock alerts: {len(stock_alerts)}, Crypto alerts: {len(crypto_alerts)}")


if __name__ == "__main__":
    main()
