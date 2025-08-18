# backend/providers/fmp.py
# Financial Modeling Prep (FMP) provider
import os
import requests


API_KEY = os.getenv("FMP_API_KEY")
BASE_URL = "https://financialmodelingprep.com/api/v3"


def fetch_most_active(limit: int = 50):
    """
    Fetch the most active stocks by trading volume.
    Returns a list of stock symbols.
    """
    if not API_KEY:
        print("⚠️ FMP_API_KEY not set, cannot fetch most active stocks")
        return []

    url = f"{BASE_URL}/stock_market/actives?apikey={API_KEY}"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        symbols = [item["symbol"] for item in data[:limit] if "symbol" in item]
        return symbols
    except Exception as e:
        print("⚠️ Error fetching most active from FMP:", e)
        return []
