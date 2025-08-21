
import os
import requests

API_KEY = os.environ.get("FMP_API_KEY")

def fetch_most_active():
    url = f"https://financialmodelingprep.com/api/v3/stock/actives?apikey={API_KEY}"
    r = requests.get(url)
    r.raise_for_status()
    data = r.json()
    # Keep only useful info
    stocks = [
        {
            "ticker": s.get("ticker"),
            "price": s.get("price"),
            "change": s.get("changes"),
            "changePercent": s.get("changesPercentage"),
            "volume": s.get("volume")
        }
        for s in data.get("mostActiveStock", [])
    ]
    return stocks
