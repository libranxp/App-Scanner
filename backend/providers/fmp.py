import requests
import os
import time

API_KEY = os.getenv("FMP_API_KEY")
BASE_URL = "https://financialmodelingprep.com/api/v3"

def fetch_most_active(retries=3, delay=5):
    """Fetch live most active stocks from FMP with retry/backoff"""
    url = f"{BASE_URL}/stock/actives?apikey={API_KEY}"
    for attempt in range(retries):
        r = requests.get(url, timeout=10)
        if r.status_code == 429:  # Too Many Requests
            print(f"⚠️ Rate limited by FMP (429). Retrying in {delay}s...")
            time.sleep(delay)
            delay *= 2  # exponential backoff
            continue
        try:
            r.raise_for_status()
            data = r.json()
            return [
                {
                    "symbol": stock.get("ticker"),
                    "price": stock.get("price"),
                    "change": stock.get("changes"),
                    "volume": stock.get("volume")
                }
                for stock in data.get("mostActiveStock", [])
            ]
        except Exception as e:
            print(f"❌ Error fetching data: {e}")
            return []
    print("❌ Failed after retries (API may be over quota)")
    return []
