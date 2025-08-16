import os
import json
import time
from datetime import datetime, timedelta

from backend.providers.finnhub import fetch_stock_data
from backend.providers.coingecko import fetch_crypto_data
from backend.sentiment import sentiment_score
from backend.ai_scoring import ai_score
from backend.risk import risk_assessment
from backend.telegram import send_telegram_alert

# ENV vars
STOCK_CHANNEL = os.getenv("TELEGRAM_STOCK_CHANNEL_ID")
CRYPTO_CHANNEL = os.getenv("TELEGRAM_CRYPTO_CHANNEL_ID")

TRIGGER_LOG = "docs/data/trigger_log.json"
STOCK_OUTPUT = "docs/data/latest_stocks.json"
CRYPTO_OUTPUT = "docs/data/latest_crypto.json"

# ✅ load last alerts to prevent duplicates
def load_trigger_log():
    if not os.path.exists(TRIGGER_LOG):
        return {}
    with open(TRIGGER_LOG, "r") as f:
        return json.load(f)

def save_trigger_log(log):
    with open(TRIGGER_LOG, "w") as f:
        json.dump(log, f, indent=2)

def passes_stock_filters(stock):
    return (
        stock["price"] > 0.04
        and stock["volume"] > 500_000
        and stock["change_percent"] > 1
        and stock["rvol"] > 1.2
        and 45 <= stock["rsi"] <= 75
        and stock["ema5"] > stock["ema13"] > stock["ema50"]
        and abs(stock["vwap_proximity"]) <= 0.015
        and stock["sentiment"] >= 0.6
        and not stock["pump_flag"]
    )

def passes_crypto_filters(coin):
    return (
        0.001 <= coin["price"] <= 100
        and coin["volume"] > 10_000_000
        and 2 <= coin["change_percent"] <= 20
        and 10_000_000 <= coin["market_cap"] <= 5_000_000_000
        and 50 <= coin["rsi"] <= 70
        and coin["rvol"] > 2
        and coin["ema5"] > coin["ema13"] > coin["ema50"]
        and abs(coin["vwap_proximity"]) <= 0.02
        and coin["sentiment"] >= 0.6
        and not coin["pump_flag"]
    )

def run_scan():
    log = load_trigger_log()
    now = datetime.utcnow()

    stocks = fetch_stock_data()
    cryptos = fetch_crypto_data()

    stock_alerts, crypto_alerts = [], []

    # 🔎 STOCKS
    for stock in stocks:
        if passes_stock_filters(stock):
            if stock["ticker"] not in log or now - datetime.fromisoformat(log[stock["ticker"]]) > timedelta(hours=6):
                stock["ai_score"] = ai_score(stock)
                stock["risk"] = risk_assessment(stock)
                stock["reason"] = "Strong RSI + volume + catalyst validation"
                stock_alerts.append(stock)
                log[stock["ticker"]] = now.isoformat()
                send_telegram_alert(STOCK_CHANNEL, stock, "stock")

    # 🔎 CRYPTOS
    for coin in cryptos:
        if passes_crypto_filters(coin):
            if coin["symbol"] not in log or now - datetime.fromisoformat(log[coin["symbol"]]) > timedelta(hours=6):
                coin["ai_score"] = ai_score(coin)
                coin["risk"] = risk_assessment(coin)
                coin["reason"] = "Strong RSI + sentiment + catalyst validation"
                crypto_alerts.append(coin)
                log[coin["symbol"]] = now.isoformat()
                send_telegram_alert(CRYPTO_CHANNEL, coin, "crypto")

    save_trigger_log(log)

    # ✅ save results for dashboard
    with open(STOCK_OUTPUT, "w") as f:
        json.dump(stock_alerts, f, indent=2)
    with open(CRYPTO_OUTPUT, "w") as f:
        json.dump(crypto_alerts, f, indent=2)

if __name__ == "__main__":
    run_scan()
