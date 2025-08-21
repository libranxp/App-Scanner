# backend/providers/alphavantage.py
import os, requests

API = os.getenv("ALPHAVANTAGE_API_KEY")

def fetch_crypto_ohlcv(symbol: str, market: str = "USD", interval: str = "5min"):
    """
    Returns dict {t,o,h,l,c,v, change_24h}
    """
    url = "https://www.alphavantage.co/query"
    params = {"function": "CRYPTO_INTRADAY", "symbol": symbol, "market": market, "interval": interval, "apikey": API}
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    j = r.json()
    key = f"Time Series Crypto ({interval})"
    ts = j.get(key, {})
    if not ts: return None
    # Sort ascending by timestamp
    items = sorted(ts.items())
    t, o, h, l, c, v = [], [], [], [], [], []
    for ts_k, vals in items:
        t.append(ts_k)
        o.append(float(vals.get("1. open", 0.0)))
        h.append(float(vals.get("2. high", 0.0)))
        l.append(float(vals.get("3. low", 0.0)))
        c.append(float(vals.get("4. close", 0.0)))
        v.append(float(vals.get("5. volume", 0.0)))
    change_24h = 0.0
    if len(c) > 0:
        first = c[0]; last = c[-1]
        if first > 0: change_24h = (last - first) / first * 100.0
    return {"t": t, "o": o, "h": h, "l": l, "c": c, "v": v, "change_24h": change_24h}
