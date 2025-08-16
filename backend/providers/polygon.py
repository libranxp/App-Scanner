import os
import requests

API_KEY = os.getenv("POLYGON_API_KEY")
BASE = "https://api.polygon.io/v2"

def fetch_aggregates(ticker="AAPL", multiplier=1, timespan="day", limit=5):
    url = f"{BASE}/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/2023-01-01/2023-12-31"
    r = requests.get(url, params={"apiKey": API_KEY, "limit": limit})
    return r.json() if r.status_code == 200 else {}
