# backend/scanner.py
import os
import time
import datetime
from backend import telegram
from backend.providers import finnhub, fmp, coingecko, polygon, alphavantage, newsapi, twitter, reddit, lunarcrush, coinmarketcal, santiment, coinglass, messari
from backend.sentiment import analyze_sentiment
from backend.risk import evaluate_risk
from backend.ai_scoring import ai_score

# Telegram channels
TELEGRAM_STOCKS_CHANNEL = os.getenv("TELEGRAM_STOCK_CHANNEL")
TELEGRAM_CRYPTO_CHANNEL = os.getenv("TELEGRAM_CRYPTO_CHANNEL")

# BST timezone helper
def current_time_bst():
    return datetime.datetime.now(datetime.timezone.utc).astimezone(
        datetime.timezone(datetime.timedelta(hours=1))
    )

# Fetch live tickers dynamically
def fetch_live_data():
    data = {"stocks": [], "crypto": []}

    try:
        stocks_data = finnhub.get_movers() + fmp.get_movers() + polygon.get_movers()
        data["stocks"].extend(stocks_data)
    except Exception as e:
        print(f"⚠️ Stock fetch error: {e}")

    try:
        crypto_data = coingecko.get_trending() + messari.get_assets() + lunarcrush.get_movers()
        data["crypto"].extend(crypto_data)
    except Exception as e:
        print(f"⚠️ Crypto fetch error: {e}")

    return data

# Process each ticker dynamically
def process_ticker(ticker_info, asset_type="stock"):
    ticker = ticker_info.get("symbol")
    sentiment_score = analyze_sentiment(ticker)
    risk_score = evaluate_risk(ticker)
    ai_result = ai_score(ticker, sentiment_score, risk_score)

    return {
        "symbol": ticker,
        "price": ticker_info.get("price"),
        "change": ticker_info.get("change"),
        "sentiment": sentiment_score,
        "risk": risk_score,
        "ai_score": ai_result,
        "asset_type": asset_type,
    }

# Send Telegram alert
def send_alert(result):
    msg = (
        f"🚨 New Signal: {result['symbol']}\n\n"
        f"📈 Price: {result['price']} | Change: {result['change']}%\n"
        f"📊 AI Score: {result['ai_score']}/10\n"
        f"🧠 Reason: Trending on social + Technical breakout\n"
        f"📍 Risk: SL = TBD | TP = TBD | Position Size = TBD\n"
        f"📡 Sentiment: {result['sentiment']}\n"
        f"📰 Catalyst: Live news, tweets, or events\n\n"
        f"🔗 TradingView Chart\n"
        f"🔗 News Source\n"
        f"🔗 Reddit Thread\n"
        f"🔗 Tweet\n\n"
        f"📅 Time: {current_time_bst().strftime('%Y-%m-%d %H:%M:%S BST')}"
    )

    chat_id = TELEGRAM_STOCKS_CHANNEL if result["asset_type"] == "stock" else TELEGRAM_CRYPTO_CHANNEL

    telegram.send_telegram_message(chat_id, msg, result["symbol"], result["asset_type"])

# Main scanner loop
def run_scanner():
    print(f"🔄 Scanner started at {current_time_bst()}")
    live_data = fetch_live_data()

    for stock in live_data["stocks"]:
        try:
            result = process_ticker(stock, "stock")
            send_alert(result)
        except Exception as e:
            print(f"⚠️ Stock processing error: {e}")

    for coin in live_data["crypto"]:
        try:
            result = process_ticker(coin, "crypto")
            send_alert(result)
        except Exception as e:
            print(f"⚠️ Crypto processing error: {e}")

    print(f"✅ Scanner finished at {current_time_bst()}")

if __name__ == "__main__":
    run_scanner()
