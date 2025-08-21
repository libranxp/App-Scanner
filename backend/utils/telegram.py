import os
import requests

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_message(text: str):
    if not BOT_TOKEN or not CHAT_ID:
        print("⚠️ Telegram not configured, skipping alert")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        r = requests.post(url, data={"chat_id": CHAT_ID, "text": text})
        if r.status_code != 200:
            print(f"❌ Telegram error: {r.text}")
    except Exception as e:
        print(f"❌ Telegram exception: {e}")
