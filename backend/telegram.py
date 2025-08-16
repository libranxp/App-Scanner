# backend/telegram.py
import requests
import os

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
STOCK_CHANNEL = os.getenv("TELEGRAM_STOCK_CHANNEL_ID")
CRYPTO_CHANNEL = os.getenv("TELEGRAM_CRYPTO_CHANNEL_ID")

def send_telegram_message(message, channel="stock"):
    if channel == "stock":
        chat_id = STOCK_CHANNEL
    else:
        chat_id = CRYPTO_CHANNEL
    if not BOT_TOKEN or not chat_id:
        print("Telegram bot token or chat ID not set.")
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
    try:
        response = requests.post(url, data=data)
        if response.status_code != 200:
            print("Telegram message failed:", response.text)
    except Exception as e:
        print("Telegram error:", e)
