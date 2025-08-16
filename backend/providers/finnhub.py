import os
import requests

API_KEY = os.getenv("FINNHUB_API_KEY")
BASE = "https://finnhub.io/api/v1"

def fetch_stock_data(exchange="US"):
    url = f"{BASE}/stock/symbol?exchange={exchange}&token={API_KEY}"
    r = requests.get(url)
    if r.status_code != 200:
        return []
    symbols = [s["symbol"] for s in r.json()[:50]]  # grab first 50

    results = []
    for symbol in symbols:
        q = requests.get(f"{BASE}/quote?symbol={symbol}&token={API_KEY}").json()
        if "c" not in q:  # skip if no data
            continue
        results.append({
            "ticker": symbol,
            "price": q.get("c"),
            "change_percent": q.get("dp"),
            "volume": q.get("v"),
            "open": q.get("o"),
            "high": q.get("h"),
            "low": q.get("l"),
            "prev_close": q.get("pc")
        })
    return results
