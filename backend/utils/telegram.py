import os
import requests

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_alert(message):
    if not TOKEN or not CHAT_ID:
        print("Telegram credentials missing")
        return
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    r = requests.post(url, data=payload)
    if r.status_code == 200:
        print("📩 Telegram alert sent:", message)
    else:
        print("Failed to send Telegram alert:", r.text)
