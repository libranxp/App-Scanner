# backend/providers/fmp.py
import os
import requests

API_KEY = os.getenv("FMP_API_KEY", "")

def fetch_most_active():
    url = f"https://financialmodelingprep.com/api/v3/stock_market/actives?apikey={API_KEY}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return [
            {
                "symbol": stock.get("symbol"),
                "price": stock.get("price"),
                "changesPercentage": stock.get("changesPercentage"),
                "volume": stock.get("volume")
            }
            for stock in data
        ]
    except Exception as e:
        print(f"FMP error: {e}")
        return []
