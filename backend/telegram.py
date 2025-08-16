import os
import requests

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def send_telegram_alert(channel_id, data, asset_type):
    if not channel_id:
        return
    
    msg = f"""
🚨 {asset_type.upper()} ALERT 🚨
{data.get('ticker', data.get('symbol'))}
💵 Price: {data['price']} ({data['change_percent']}%)
📊 RSI: {data['rsi']} | RVOL: {data['rvol']} | VWAP Prox: {data['vwap_proximity']}
🤖 AI Score: {data['ai_score']} ({data['reason']})
⚠️ Risk: {data['risk']}
🔗 [Sentiment]({data['sentiment_link']}) | [Catalyst]({data['catalyst_link']}) | [News]({data['news_link']}) | [TradingView]({data['tradingview_link']})
"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": channel_id, "text": msg, "parse_mode": "Markdown"}
    requests.post(url, json=payload)
