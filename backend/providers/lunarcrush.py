import os
import requests

API_KEY = os.getenv("LUNARCRUSH_API_KEY")
BASE = "https://lunarcrush.com/api3"

def fetch_social_data(symbol="BTC"):
    url = f"{BASE}/assets"
    r = requests.get(url, params={"data": "assets", "symbol": symbol, "key": API_KEY})
    return r.json() if r.status_code == 200 else {}
