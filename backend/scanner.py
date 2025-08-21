import os
import json
from backend.providers import fmp
from backend.utils import telegram

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))

def save_dashboard(stocks):
    json_path = os.path.join(ROOT_DIR, "dashboard.json")
    html_path = os.path.join(ROOT_DIR, "dashboard.html")

    with open(json_path, "w") as f:
        json.dump(stocks, f, indent=2)

    # Generate simple HTML
    with open(html_path, "w") as f:
        f.write("<html><head><title>Stock Dashboard</title></head><body>")
        f.write("<h1>Most Active Stocks</h1><table border='1'><tr><th>Ticker</th><th>Price</th><th>Changes</th></tr>")
        for s in stocks:
            f.write(f"<tr><td>{s.get('ticker')}</td><td>{s.get('price')}</td><td>{s.get('changes')}</td></tr>")
        f.write("</table></body></html>")

    print(f"✅ Saved dashboard.json & dashboard.html")

def run_scan():
    print("🔍 Fetching live stock data...")
    stocks = fmp.fetch_most_active()

    if not stocks:
        print("⚠️ No stocks fetched, writing empty dashboard")
        save_dashboard([])
        return

    save_dashboard(stocks)

    # Telegram alert
    first5 = [s["ticker"] for s in stocks[:5]]
    telegram.send_message(f"📊 Top active stocks: {', '.join(first5)}")

if __name__ == "__main__":
    run_scan()
