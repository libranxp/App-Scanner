import json
import os
from backend.providers import fmp
from backend.utils.telegram import send_telegram_message

def save_dashboard(data, path="dashboard.json"):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Dashboard updated at {os.path.abspath(path)}")

def run_scan():
    print("🔍 Fetching live stock data...")
    stocks = fmp.fetch_most_active()

    if not stocks:
        print("⚠️ No data fetched")
        return

    save_dashboard(stocks)

    # Example: send alert if >5% move
    for stock in stocks:
        if abs(stock.get("change", 0)) > 5:
            send_telegram_message(
                f"🚀 {stock['symbol']} moved {stock['change']}% (Price: {stock['price']})"
            )

if __name__ == "__main__":
    run_scan()
