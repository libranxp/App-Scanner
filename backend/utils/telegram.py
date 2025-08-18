# backend/utils/telegram.py
# Utility for sending Telegram messages

import os
import requests
import json


def send_telegram_message(alert: dict):
    """
    Send an alert to Telegram channel.
    Requires environment variables:
      - TELEGRAM_BOT_TOKEN
      - TELEGRAM_STOCK_CHANNEL_ID or TELEGRAM_CRYPTO_CHANNEL_ID
    """
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    stock_channel = os.getenv("TELEGRAM_STOCK_CHANNEL_ID")
    crypto_channel = os.getenv("TELEGRAM_CRYPTO_CHANNEL_ID")

    if not token:
        print("⚠️ TELEGRAM_BOT_TOKEN not set, skipping message")
        return

    # Decide which chat_id to use
    chat_id = stock_channel if alert.get("asset_type") == "stock" else crypto_channel
    if not chat_id:
        print("⚠️ No TELEGRAM channel ID provided for", alert.get("asset_type"))
        return

    # Build message text
    text = (
        f"📢 Alert: {alert.get('symbol')}\n"
        f"Type: {alert.get('asset_type')}\n"
        f"Price: {alert.get('price')}\n"
        f"Sentiment: {alert.get('sentiment')}\n"
        f"AI Score: {alert.get('ai_score')}\n"
        f"Risk: {alert.get('risk')}"
    )

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}

    try:
        r = requests.post(url, json=payload, timeout=10)
        if r.status_code != 200:
            print(f"⚠️ Telegram error {r.status_code}: {r.text}")
    except Exception as e:
        print("⚠️ Failed to send Telegram message:", e)
