import os
import requests

API_KEY = os.getenv("FMP_API_KEY")

def fetch_most_active():
    url = f"https://financialmodelingprep.com/api/v3/stock/actives?apikey={API_KEY}"
    try:
        r = requests.get(url)
        if r.status_code == 429:
            print("⚠️ Rate limit hit on FMP API")
            return []
        r.raise_for_status()
        data = r.json()
        return data.get("mostActiveStock", [])
    except Exception as e:
        print(f"❌ Error fetching FMP data: {e}")
        return []
