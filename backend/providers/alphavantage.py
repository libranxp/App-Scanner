import os
import requests

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")
BASE = "https://www.alphavantage.co/query"

def fetch_rsi(ticker, interval="15min"):
    url = f"{BASE}?function=RSI&symbol={ticker}&interval={interval}&time_period=14&series_type=close&apikey={API_KEY}"
    r = requests.get(url)
    data = r.json()
    try:
        latest = list(data["Technical Analysis: RSI"].values())[0]
        return float(latest["RSI"])
    except Exception:
        return None

def fetch_ema(ticker, time_period=13, interval="15min"):
    url = f"{BASE}?function=EMA&symbol={ticker}&interval={interval}&time_period={time_period}&series_type=close&apikey={API_KEY}"
    r = requests.get(url)
    data = r.json()
    try:
        latest = list(data["Technical Analysis: EMA"].values())[0]
        return float(latest["EMA"])
    except Exception:
        return None
