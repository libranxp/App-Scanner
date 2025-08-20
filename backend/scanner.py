# backend/scanner.py
import json
import os
from backend.providers import fmp
from backend.utils.telegram import send_telegram_message

DASHBOARD_FILE = "dashboard.json"

def run_scan():
    try:
        stock_symbols = fmp.fetch_most_active()  # API-driven
    except Exception as e:
        print(f"Error fetching symbols: {e}")
        stock_symbols = []

    dashboard_data = {
        "stocks": stock_symbols if stock_symbols else [],
        "meta": {"status": "ok", "count": len(stock_symbols)}
    }

    # ✅ Always write dashboard.json (so file exists)
    with open(DASHBOARD_FILE, "w") as f:
        json.dump(dashboard_data, f, indent=2)

    # ✅ Send Telegram alert if results exist
    if stock_symbols:
        msg = f"📊 Scanner found {len(stock_symbols)} active stocks."
        send_telegram_message(msg)
    else:
        send_telegram_message("⚠️ Scanner ran but found no data.")

if __name__ == "__main__":
    run_scan()
