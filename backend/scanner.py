import json
from datetime import datetime
from backend.providers import fmp
from backend.utils.telegram import send_telegram_message

DASHBOARD_FILE = "dashboard.json"

def update_dashboard(data):
    """Write fresh stock data to dashboard.json for frontend to load."""
    with open(DASHBOARD_FILE, "w") as f:
        json.dump(data, f, indent=2)

def run_scan():
    print("🚀 Running live stock scan...")

    try:
        stocks = fmp.fetch_most_active()
    except Exception as e:
        print(f"⚠️ Error fetching stock data: {e}")
        update_dashboard([])  # write empty so frontend won't crash
        return

    if not stocks:
        print("⚠️ No data returned from API")
        update_dashboard([])
        return

    results = []
    for stock in stocks:
        symbol = stock.get("symbol")
        price = stock.get("price")
        change = stock.get("changesPercentage")

        if not symbol or price is None:
            continue

        entry = {
            "symbol": symbol,
            "price": price,
            "change": change,
            "last_updated": datetime.utcnow().isoformat()
        }
        results.append(entry)

        # ✅ Send alert for each stock
        msg = f"📊 {symbol} | Price: {price} | Change: {change}%"
        send_telegram_message(msg, channel="stock")

    # ✅ Always update dashboard
    update_dashboard(results)
    print(f"✅ Dashboard updated with {len(results)} entries")

if __name__ == "__main__":
    run_scan()
