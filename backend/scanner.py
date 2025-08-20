import json
import os
from datetime import datetime
from backend.providers import fmp
from backend.utils.telegram import send_telegram_message

DASHBOARD_FILE = "dashboard.json"

def update_dashboard(data):
    """Write latest stock data to dashboard.json"""
    with open(DASHBOARD_FILE, "w") as f:
        json.dump(data, f, indent=2)

def run_scan():
    print("🚀 Running live scan...")
    stocks = fmp.fetch_most_active()

    if not stocks:
        print("⚠️ No stock data fetched")
        return

    results = []
    for stock in stocks:
        symbol = stock.get("symbol")
        price = stock.get("price")
        change = stock.get("changesPercentage")

        entry = {
            "symbol": symbol,
            "price": price,
            "change": change,
            "time": datetime.utcnow().isoformat()
        }
        results.append(entry)

        # ✅ Send to Telegram
        msg = f"📊 {symbol} | Price: {price} | Change: {change}%"
        send_telegram_message(msg, channel="stock")

    # ✅ Update dashboard file
    update_dashboard(results)
    print(f"✅ Dashboard updated with {len(results)} entries")

if __name__ == "__main__":
    run_scan()
