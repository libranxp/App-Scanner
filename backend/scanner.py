import os
import json
from backend.providers import fmp, finnhub, alphavantage, polygon
from backend.utils import telegram

def run_scan():
    results = {
        "stocks": [],
        "crypto": []
    }

    # --- STOCKS (FMP, Finnhub, Polygon) ---
    try:
        stocks = fmp.fetch_premarket()
        results["stocks"].extend(stocks)
    except Exception as e:
        print("⚠️ FMP error:", e)

    try:
        finn = finnhub.fetch_active()
        results["stocks"].extend(finn)
    except Exception as e:
        print("⚠️ Finnhub error:", e)

    try:
        poly = polygon.fetch_gainers()
        results["stocks"].extend(poly)
    except Exception as e:
        print("⚠️ Polygon error:", e)

    # --- CRYPTO (LunarCrush, Messari, CoinMarketCal, etc.) ---
    try:
        # Example: Replace with actual provider methods
        from backend.providers import lunarcrush, messari, coinmarketcal
        crypto = lunarcrush.fetch_trending()
        results["crypto"].extend(crypto)
    except Exception as e:
        print("⚠️ LunarCrush error:", e)

    # Save dashboard.json
    with open("dashboard.json", "w") as f:
        json.dump(results, f, indent=2)
    print("✅ Dashboard saved")

    # --- Telegram alerts ---
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    stocks_chat = os.getenv("TELEGRAM_STOCKS_CHANNEL_ID")
    crypto_chat = os.getenv("TELEGRAM_CRYPTO_CHANNEL_ID")

    if token and stocks_chat:
        telegram.send_message(token, stocks_chat, "📊 Stocks scan complete")
    if token and crypto_chat:
        telegram.send_message(token, crypto_chat, "💰 Crypto scan complete")

if __name__ == "__main__":
    run_scan()
