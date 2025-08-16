# backend/telegram.py
import os
import requests

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def send_telegram_message(chat_id, message, ticker=None, asset_type="stock"):
    """
    Sends a Telegram message via bot.
    """
    if not TELEGRAM_BOT_TOKEN or not chat_id:
        print("⚠️ Telegram token or chat ID not set")
        return

    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print(f"⚠️ Telegram error: {response.text}")
    except Exception as e:
        print(f"⚠️ Telegram exception: {e}")
