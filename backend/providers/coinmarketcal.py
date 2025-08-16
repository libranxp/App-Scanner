import os
import requests

API_KEY = os.getenv("COINMARKETCAL_API_KEY")
BASE = "https://developers.coinmarketcal.com/v1/events"

def fetch_crypto_events(limit=10):
    headers = {"x-api-key": API_KEY}
    r = requests.get(BASE, headers=headers, params={"max": limit})
    return r.json().get("body", []) if r.status_code == 200 else []
