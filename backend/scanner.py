import os
from tier1 import get_premarket_gainers
from tier2 import enrich_with_catalysts
from telegram import send_telegram_message
from datetime import datetime

TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

def run_daily_scan():
    gainers = get_premarket_gainers()
    enriched_list = []

    for stock in gainers:
        enriched = enrich_with_catalysts(stock["symbol"])
        enriched.update(stock)
        enriched_list.append(enriched)

        # Send Telegram alert
        message = f"📈 {enriched['symbol']} | Price: {enriched['price']} | Gap: {enriched['gap']}%\nNews: {len(enriched['news'])} articles"
        send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, message)

    return enriched_list

if __name__ == "__main__":
    results = run_daily_scan()
    print(f"Scan completed at {datetime.now()}")
