# backend/utils/telegram.py
import requests
import time

def _post(token: str, method: str, payload: dict):
    url = f"https://api.telegram.org/bot{token}/{method}"
    r = requests.post(url, json=payload, timeout=20)
    r.raise_for_status()
    return r.json()

def send_message(token: str, chat_id: str, text: str):
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    try:
        _post(token, "sendMessage", payload)
    except Exception as e:
        print(f"⚠️ Telegram send_message error: {e}")

def send_signal(token: str, chat_id: str, s: dict):
    """
    s fields expected:
      symbol, price, change_pct, ai_score, confidence, reason,
      sl, tp, position_size, sentiment_label,
      tradingview_url, news_url, reddit_url, tweet_url,
      catalyst_url, time_bst
    """
    text = (
        f"🚨 *New Signal: ${s['symbol']}*\n\n"
        f"📈 *Price:* ${s['price']:.4f} | *Change:* {s['change_pct']:+.2f}%\n"
        f"📊 *AI Score:* {s['ai_score']:.1f}/10 ({s['confidence']})\n"
        f"🧠 *Reason:* {s['reason']}\n"
        f"📍 *Risk:* SL = ${s['sl']:.4f} | TP = ${s['tp']:.4f} | Position Size: ${s['position_size']}\n"
        f"📡 *Sentiment:* {s['sentiment_label']}\n"
        f"📰 *Catalyst:* {s['catalyst_label']}\n\n"
        f"🔗 [TradingView Chart]({s['tradingview_url']})\n"
        f"🔗 [News Source]({s['news_url']})\n"
        f"🔗 [Reddit Thread]({s['reddit_url']})\n"
        f"🔗 [Tweet]({s['tweet_url']})\n\n"
        f"📅 *Time:* {s['time_bst']}"
    )
    send_message(token, chat_id, text)

def throttle(seconds: float):
    time.sleep(seconds)
