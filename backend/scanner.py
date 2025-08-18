# backend/scanner.py
import os
import json
from backend.providers import fmp
from backend.sentiment import sentiment_score
from backend.ai_scoring import ai_score
from backend.risk import risk_assessment
from backend.utils.telegram import send_telegram_message


TRIGGER_LOG = "trigger_log.json"


def load_trigger_log():
    if not os.path.exists(TRIGGER_LOG):
        return {}
    try:
        with open(TRIGGER_LOG, "r") as f:
            return json.load(f)
    except Exception:
        return {}


def save_trigger_log(log):
    with open(TRIGGER_LOG, "w") as f:
        json.dump(log, f)


def run_scan():
    log = load_trigger_log()

    # ✅ get real most active tickers (no samples)
    stock_symbols = fmp.fetch_most_active(limit=20)

    for symbol in stock_symbols:
        try:
            sentiment = sentiment_score(symbol)
            ai = ai_score(symbol)
            risk = risk_assessment(symbol)

            alert = {
                "symbol": symbol,
                "asset_type": "stock",
                "price": "N/A",  # you can extend this with price fetcher
                "sentiment": sentiment,
                "ai_score": ai,
                "risk": risk,
            }

            # send to telegram
            send_telegram_message(alert)

            # update log
            log[symbol] = alert

        except Exception as e:
            print(f"⚠️ Error scanning {symbol}:", e)

    save_trigger_log(log)


if __name__ == "__main__":
    run_scan()
