import os
import requests

API_KEY = os.getenv("MESSARI_API_KEY")
BASE = "https://data.messari.io/api/v1"

def fetch_asset_metrics(symbol="btc"):
    url = f"{BASE}/assets/{symbol}/metrics"
    headers = {"x-messari-api-key": API_KEY}
    r = requests.get(url, headers=headers)
    return r.json() if r.status_code == 200 else {}
