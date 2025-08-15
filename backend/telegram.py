import os
import requests

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID_STOCKS = os.getenv("TELEGRAM_CHAT_ID_STOCKS")
CHAT_ID_CRYPTO = os.getenv("TELEGRAM_CHAT_ID_CRYPTO")

def send_telegram_message(text, is_crypto=False):
    chat_id = CHAT_ID_CRYPTO if is_crypto else CHAT_ID_STOCKS
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)
