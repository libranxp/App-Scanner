import os
import requests

API_KEY = os.getenv("FMP_API_KEY")
BASE_URL = "https://financialmodelingprep.com/api/v3"

def fetch_most_active():
    """Fetch most active stocks from FMP API (live data only)."""
    if not API_KEY:
        raise ValueError("Missing FMP_API_KEY environment variable")

    url = f"{BASE_URL}/stock_market/actives?apikey={API_KEY}"
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()

    data = resp.json()
    if not isinstance(data, list):
        return []
    return data
