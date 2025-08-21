# backend/providers/finnhub.py
import os, time, requests

API = os.getenv("FINNHUB_API_KEY")

def fetch_ohlcv(symbol: str, resolution: str = "5", lookback_minutes: int = 800):
    """Fetch recent candles for indicators. resolution '1','5','15'..."""
    now = int(time.time())
    frm = now - lookback_minutes * 60
    url = f"https://finnhub.io/api/v1/stock/candle?symbol={symbol}&resolution={resolution}&from={frm}&to={now}&token={API}"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    j = r.json()
    if j.get("s") != "ok":
        return None
    return {
        "t": j["t"],
        "o": j["o"],
        "h": j["h"],
        "l": j["l"],
        "c": j["c"],
        "v": j["v"],
    }

def fetch_price(symbol: str):
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={API}"
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    j = r.json()
    return float(j.get("c") or 0.0), float(j.get("dp") or 0.0)
