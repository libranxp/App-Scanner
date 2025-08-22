import os
import requests
from utils.util import format_price, get_timestamp

# Load secrets from environment variables
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_CRYPTO = os.getenv("TELEGRAM_CRYPTO_CHANNEL_ID")
CHANNEL_STOCKS = os.getenv("TELEGRAM_STOCKS_CHANNEL_ID")

def format_alert(data):
    ticker = data["ticker"]
    price = format_price(data["price"])
    change = f"{data['change']}%"
    ai_score = data["ai_score"]
    confidence = data["confidence"]
    narrative = data["narrative"]
    risk = data["risk"]
    sentiment = data["sentiment"]
    catalyst = data["catalyst"]
    timestamp = get_timestamp()

    return f"""
🚨 *New Signal: ${ticker}*

📈 *Price*: {price} | *Change*: {change}
📊 *AI Score*: {ai_score}/10 ({confidence})
🧠 *Reason*: _{narrative}_
📍 *Risk*: SL = {format_price(risk['stop_loss'])} | TP = {format_price(risk['take_profit'])} | Size = ${risk['position_size']}

📡 *Sentiment*: {sentiment['score']} (Twitter + Reddit + News)
📰 *Catalyst*: {catalyst.get('tweet') or 'No tweet'} + {catalyst.get('headline') or 'No headline'}

🔗 [TradingView Chart](https://www.tradingview.com/symbols/{ticker})
🔗 [News](https://newsapi.org/article)
🔗 [Reddit](https://reddit.com/r/{'cryptocurrency' if data['asset_type'] == 'crypto' else 'stocks'})
🔗 [Tweet](https://twitter.com/search?q={ticker})

📅 *Time*: {timestamp}
""".strip()

def send_telegram_alert(data):
    message = format_alert(data)
    channel_id = CHANNEL_CRYPTO if data["asset_type"] == "crypto" else CHANNEL_STOCKS
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": channel_id,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            print(f"Telegram alert failed: {response.text}")
    except Exception as e:
        print(f"Telegram alert error: {str(e)}")
