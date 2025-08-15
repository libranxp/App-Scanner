import requests, json
from backend.util import getenv


BOT = getenv('TELEGRAM_BOT_TOKEN')
CHAT_STOCKS = getenv('TELEGRAM_CHAT_ID_STOCKS')
CHAT_CRYPTO = getenv('TELEGRAM_CHAT_ID_CRYPTO')


API = f'https://api.telegram.org/bot{BOT}' if BOT else None


def send_message(text, is_crypto=False):
if not API:
return {'ok': False, 'error': 'No TELEGRAM_BOT_TOKEN configured'}
chat = CHAT_CRYPTO if is_crypto else CHAT_STOCKS
if not chat:
return {'ok': False, 'error': 'Missing chat id'}
r = requests.post(f'{API}/sendMessage', json={'chat_id': chat, 'text': text, 'parse_mode': 'Markdown'}, timeout=20)
try:
r.raise_for_status()
return r.json()
except Exception as e:
return {'ok': False, 'error': str(e), 'status': getattr(r, 'status_code', None), 'body': r.text}




def format_alert(signal):
# signal contains: ticker/symbol, price, change, ai_score, reason, risk, sentiment, links, time
lines = []
lines.append(f"🚨 *New Signal:* ${signal.get('symbol','?')}")
lines.append("")
lines.append(f"📈 Price: ${signal.get('price','?')} | Change: {signal.get('change','?')}")
lines.append(f"📊 AI Score: {signal.get('ai_score','?')}/10 ({signal.get('ai_confidence','')})")
if signal.get('ai_validation'):
lines.append(f"🧠 Reason: _{signal['ai_validation']}_")
risk = signal.get('risk', {})
lines.append(f"📍 Risk: SL = ${risk.get('sl','?')} | TP = ${risk.get('tp','?')} | Position Size: ${risk.get('size','?')}")
lines.append(f"📡 Sentiment: {signal.get('sentiment_label','Neutral')} (Twitter+Reddit+News)")
cat = signal.get('catalyst', {})
cat_bits = []
if cat.get('top_headline'): cat_bits.append('News')
if cat.get('insider'): cat_bits.append('Insider')
if cat.get('calendar_events'): cat_bits.append('Calendar')
if cat_bits:
lines.append(f"📰 Catalyst: {', '.join(cat_bits)}")
# Links
if signal.get('tv_symbol'):
lines.append(f"🔗 [TradingView Chart](https://www.tradingview.com/symbols/{signal['tv_symbol']}/)")
if cat.get('top_url'):
lines.append(f"🔗 [News Source]({cat['top_url']})")
# Timestamp
lines.append(f"\n📅 Time: {signal.get('time_bst','')} BST")
return "\n".join(lines)
