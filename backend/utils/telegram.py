import requests
import os

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_CRYPTO = os.getenv("TELEGRAM_CRYPTO_CHANNEL_ID")
CHANNEL_STOCKS = os.getenv("TELEGRAM_STOCKS_CHANNEL_ID")

def send_alert(data):
    ticker = data["ticker"]
    asset_type = data["asset_type"]
    channel_id = CHANNEL_CRYPTO if asset_type == "crypto" else CHANNEL_STOCKS

    message = f"""
🚨 *New Signal: ${ticker}*

📈 *Price*: ${data['price']:.2f} | *Change*: {data['change']}%
📊 *AI Score*: {data['ai_score']}/10 ({data['confidence']})
🧠 *Reason*: _{data['narrative']}_
📍 *Risk*: SL = ${data['risk']['stop_loss']:.2f} | TP = ${data['risk']['take_profit']:.2f} | Size = ${data['risk']['position_size']}

📡 *Sentiment*: {data['sentiment']['score']} (Twitter, Reddit, News)
📰 *Catalyst*: {data['catalyst']['headline'] or 'No headline'} + {data['catalyst']['tweet'] or 'No tweet'}

🔗 [TradingView Chart](https://www.tradingview.com/symbols/{ticker})
🔗 [News](https://newsapi.org/article)
🔗 [Reddit](https://reddit.com/r/{'cryptocurrency' if asset_type == 'crypto' else 'stocks'})
🔗 [Tweet](https://twitter.com/search?q={ticker})

📅 *Time*: {data['timestamp']}
    """

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": channel_id,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Telegram alert failed for {ticker}: {str(e)}")
