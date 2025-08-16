# backend/telegram.py
import os
import requests

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def send_telegram_message(chat_id, message, ticker=None, asset_type=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    try:
        response = requests.post(url, data=payload, timeout=10)
        if response.status_code != 200:
            print(f"⚠️ Telegram send failed: {response.text}")
    except Exception as e:
        print(f"⚠️ Telegram request error: {e}")
