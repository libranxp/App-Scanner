# backend/utils/telegram.py
import os
import requests


def send_telegram_message(alert: dict):
    """
    Send alert message to Telegram channel.
    Requires:
      - TELEGRAM_BOT_TOKEN
      - TELEGRAM_STOCK_CHANNEL_ID or TELEGRAM_CRYPTO_CHANNEL_ID
    """
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    stock_channel = os.getenv("TELEGRAM_STOCK_CHANNEL_ID")
    crypto_channel = os.getenv("TELEGRAM_CRYPTO_CHANNEL_ID")

    if not token:
        print("⚠️ No TELEGRAM_BOT_TOKEN set, skipping alert")
        return

    chat_id = stock_channel if alert.get("asset_type") == "stock" else crypto_channel
    if not chat_id:
        print("⚠️ No Telegram channel ID set for", alert.get("asset_type"))
        return

    text = (
        f"📢 Alert: {alert.get('symbol')}\n"
        f"Type: {alert.get('asset_type')}\n"
        f"Price: {alert.get('price')}\n"
        f"Sentiment: {alert.get('sentiment')}\n"
        f"AI Score: {alert.get('ai_score')}\n"
        f"Risk: {alert.get('risk')}"
    )

    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        r = requests.post(url, json={"chat_id": chat_id, "text": text}, timeout=10)
        if r.status_code != 200:
            print("⚠️ Telegram error:", r.text)
    except Exception as e:
        print("⚠️ Telegram send failed:", e)
