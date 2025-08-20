import os
import requests

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
STOCK_CHANNEL = os.getenv("TELEGRAM_STOCK_CHANNEL_ID")
CRYPTO_CHANNEL = os.getenv("TELEGRAM_CRYPTO_CHANNEL_ID")

def send_telegram_message(message: str, channel="stock"):
    """Send message to Telegram channel"""
    chat_id = STOCK_CHANNEL if channel == "stock" else CRYPTO_CHANNEL
    if not BOT_TOKEN or not chat_id:
        print("⚠️ Missing Telegram config")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    r = requests.post(url, json=payload, timeout=10)

    if r.status_code != 200:
        print(f"⚠️ Telegram error: {r.text}")
    else:
        print(f"✅ Sent to Telegram: {message}")
