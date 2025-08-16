# backend/scanner.py
import os
import time
import datetime
from backend import telegram
from backend.providers import (
    finnhub, fmp, coingecko, polygon,
    alphavantage, newsapi, twitter,
    reddit, lunarcrush, coinmarketcal,
    santiment, coinglass, messari
)
from backend.sentiment import aggregate_sentiment
from backend.risk import calculate_risk
from backend.ai_scoring import calculate_ai_score, generate_reason

# Telegram channels (set via GitHub Secrets or env)
TELEGRAM_STOCKS_CHANNEL = os.getenv("TELEGRAM_STOCKS_CHANNEL")
TELEGRAM_CRYPTO_CHANNEL = os.getenv("TELEGRAM_CRYPTO_CHANNEL")

SCAN_INTERVAL = 45 * 60  # 45 minutes


def current_time_bst():
    return datetime.datetime.now(datetime.timezone.utc).astimezone(
        datetime.timezone(datetime.timedelta(hours=1))  # BST = UTC+1
    )


def fetch_live_data():
    data = {"stocks": [], "crypto": []}

    # Stocks
    try:
        stocks = finnhub.get_live_stocks() + fmp.get_live_stocks() + polygon.get_live_stocks()
        data["stocks"].extend(stocks)
    except Exception as e:
        print(f"⚠️ Stock fetch error: {e}")

    # Crypto
    try:
        cryptos = coingecko.get_live_cryptos() + messari.get_live_cryptos() + lunarcrush.get_live_cryptos()
        data["crypto"].extend(cryptos)
    except Exception as e:
        print(f"⚠️ Crypto fetch error: {e}")

    return data


def process_ticker(ticker_info, asset_type="stock"):
    ticker = ticker_info.get("symbol")
    price = ticker_info.get("price") or 0
    change_pct = ticker_info.get("change") or 0

    # Social & news sentiment
    sentiment_score = aggregate_sentiment(ticker)

    # Risk & AI scoring
    sl, tp, position_size = calculate_risk(price, 5)  # temp AI score placeholder
    ai_score = calculate_ai_score(ticker, price, change_pct, sentiment_score, [])
    reason = generate_reason(ticker, price, change_pct, sentiment_score, [])

    # Fetch catalysts/news/social
    news_url = newsapi.get_latest_article(ticker)
    reddit_url = reddit.get_top_post(ticker)
    tweet_url = twitter.get_top_tweet(ticker)
    catalysts = coinmarketcal.get_upcoming_events(ticker)

    result = {
        "symbol": ticker,
        "price": price,
        "change": change_pct,
        "ai_score": ai_score,
        "reason": reason,
        "sl": sl,
        "tp": tp,
        "position_size": position_size,
        "sentiment": sentiment_score,
        "catalysts": catalysts,
        "news_url": news_url,
        "reddit_url": reddit_url,
        "tweet_url": tweet_url,
        "asset_type": asset_type
    }

    return result


def send_alert(result):
    chat_id = TELEGRAM_STOCKS_CHANNEL if result["asset_type"] == "stock" else TELEGRAM_CRYPTO_CHANNEL

    message = (
        f"🚨 New Signal: {result['symbol']}\n\n"
        f"📈 Price: {result['price']} | Change: {result['change']}%\n"
        f"📊 AI Score: {result['ai_score']}/10 (High Confidence)\n"
        f"🧠 Reason: {result['reason']}\n"
        f"📍 Risk: SL = {result['sl']} | TP = {result['tp']} | Position Size: ${result['position_size']}\n"
        f"📡 Sentiment: {result['sentiment']}\n"
        f"📰 Catalyst: {', '.join(result['catalysts']) if result['catalysts'] else 'None'}\n\n"
        f"🔗 TradingView Chart\n"
        f"🔗 News Source: {result['news_url']}\n"
        f"🔗 Reddit Thread: {result['reddit_url']}\n"
        f"🔗 Tweet: {result['tweet_url']}\n\n"
        f"📅 Time: {current_time_bst().strftime('%H:%M %Z')}"
    )

    telegram.send_telegram_message(chat_id=chat_id, message=message, ticker=result["symbol"], asset_type=result["asset_type"])


def run_scanner():
    print(f"🔄 Scanner started at {current_time_bst()}")
    live_data = fetch_live_data()

    # Process stocks
    for stock in live_data["stocks"]:
        try:
            result = process_ticker(stock, asset_type="stock")
            send_alert(result)
        except Exception as e:
            print(f"⚠️ Stock processing error: {e}")

    # Process crypto
    for coin in live_data["crypto"]:
        try:
            result = process_ticker(coin, asset_type="crypto")
            send_alert(result)
        except Exception as e:
            print(f"⚠️ Crypto processing error: {e}")

    print(f"✅ Scanner finished at {current_time_bst()}")


if __name__ == "__main__":
    while True:
        run_scanner()
        time.sleep(SCAN_INTERVAL)
