# backend/scanner.py
import json
from backend.providers import fmp
from backend.utils.telegram import send_telegram_message

DASHBOARD_FILE = "dashboard.json"

def run_scan():
    print("🔍 Running stock scanner...")
    try:
        stock_symbols = fmp.fetch_most_active()
    except Exception as e:
        print(f"Error fetching symbols: {e}")
        stock_symbols = []

    dashboard_data = {
        "stocks": stock_symbols,
        "meta": {"status": "ok", "count": len(stock_symbols)}
    }

    with open(DASHBOARD_FILE, "w") as f:
        json.dump(dashboard_data, f, indent=2)

    if stock_symbols:
        msg = f"📊 Scanner found {len(stock_symbols)} active stocks."
        send_telegram_message(msg)
    else:
        send_telegram_message("⚠️ Scanner ran but found no stocks.")

if __name__ == "__main__":
    run_scan()
