import os
import json
from backend.providers import fmp
from backend.utils import telegram

def run_scan():
    print("🔍 Running premarket scanner...")
    
    # Fetch stocks dynamically, no pre-picked tickers
    stocks = fmp.fetch_premarket()  

    # Save to dashboard JSON
    dashboard_file = "dashboard.json"
    with open(dashboard_file, "w") as f:
        json.dump(stocks, f, indent=2)
    print(f"✅ Dashboard saved: {dashboard_file}")

    # Send Telegram notification
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if chat_id and token:
        telegram.send_message(token, chat_id, "Scanner run complete! 📊")

if __name__ == "__main__":
    run_scan()
