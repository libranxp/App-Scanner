import requests
import os

API_KEY = os.getenv("FMP_API_KEY")
BASE_URL = "https://financialmodelingprep.com/api/v3"

def fetch_most_active():
    """Fetch live most active stocks from FMP"""
    url = f"{BASE_URL}/stock/actives?apikey={API_KEY}"
    r = requests.get(url, timeout=10)
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
