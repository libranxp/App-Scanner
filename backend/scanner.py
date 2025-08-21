import json
import time
from backend.providers import fmp
from backend.utils import telegram

DASHBOARD_FILE = "dashboard.json"

def run_scan():
    print("🔍 Fetching live stock data...")
    try:
        stocks = fmp.fetch_most_active()  # fetch live data from FMP
    except Exception as e:
        print("Error fetching stock data:", e)
        stocks = []

    # Save to dashboard.json
    try:
        with open(DASHBOARD_FILE, "w") as f:
            json.dump(stocks, f, indent=2)
        print("✅ Dashboard updated")
    except Exception as e:
        print("Error writing dashboard:", e)

    # Send Telegram alerts
    try:
        for stock in stocks:
            if stock.get("changePercent", 0) > 5:  # example alert criteria
                telegram.send_alert(f"{stock['ticker']} moved {stock['changePercent']}%")
    except Exception as e:
        print("Error sending Telegram alerts:", e)

if __name__ == "__main__":
    run_scan()
