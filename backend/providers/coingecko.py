import requests

BASE = "https://api.coingecko.com/api/v3"

def fetch_crypto_data(limit=50):
    url = f"{BASE}/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "volume_desc",
        "per_page": limit,
        "page": 1,
        "sparkline": False
    }
    r = requests.get(url)
    return r.json() if r.status_code == 200 else []
