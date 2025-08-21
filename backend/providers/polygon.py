# backend/providers/polygon.py
import os, requests

API = os.getenv("POLYGON_API_KEY")

def fetch_gainers(limit: int = 50):
    """
    Live top gainers snapshot (no pre-picked tickers).
    """
    url = f"https://api.polygon.io/v2/snapshot/locale/us/markets/stocks/gainers?apiKey={API}"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    j = r.json()
    out = []
    for it in j.get("tickers", []):
        sym = it.get("ticker")
        last = (it.get("lastTrade", {}) or {}).get("p") or it.get("day", {}).get("c")
        chg = (it.get("day", {}) or {}).get("pc")
        vol = (it.get("day", {}) or {}).get("v")
        if not sym or last is None: continue
        out.append({
            "symbol": sym.upper(),
            "price": float(last),
            "change_pct": float(chg or 0.0),
            "volume": float(vol or 0.0),
        })
    return out[:limit]
