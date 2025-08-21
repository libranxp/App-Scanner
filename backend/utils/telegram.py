import requests

def send_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    try:
        r = requests.post(url, data=payload)
        r.raise_for_status()
    except Exception as e:
        print("⚠️ Telegram message failed:", e)
