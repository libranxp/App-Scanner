import os
import requests

API_KEY = os.getenv("COINGLASS_API_KEY")
BASE = "https://open-api.coinglass.com/api"

def fetch_open_interest(symbol="BTC"):
    url = f"{BASE}/futures/openInterest"
    headers = {"coinglassSecret": API_KEY}
    r = requests.get(url, headers=headers, params={"symbol": symbol})
    return r.json() if r.status_code == 200 else {}
