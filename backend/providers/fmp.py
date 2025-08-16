import os
import requests

API_KEY = os.getenv("FMP_API_KEY")
BASE = "https://financialmodelingprep.com/api/v3"

def fetch_company_profile(ticker):
    url = f"{BASE}/profile/{ticker}?apikey={API_KEY}"
    r = requests.get(url)
    return r.json() if r.status_code == 200 else []
