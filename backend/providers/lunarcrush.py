# backend/providers/lunarcrush.py
import os, requests

API = os.getenv("LUNARCRUSH_API_KEY")

def fetch_trending(limit: int = 50):
    """
    Live trending crypto by social activity (no pre-picked tickers).
    """
    url = f"https://lunarcrush.com/api3/coins?limit={limit}&sort=galaxy_score:desc&data_points=0&key={API}"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    j = r.json()
    out = []
    for it in j.get("data", []):
        sym = (it.get("symbol") or "").upper()
        price = it.get("price")
        vol24 = it.get("volume_24h")
        mentions = it.get("social_volume")
        if not sym or price is None: continue
        out.append({
            "symbol": sym,
            "price": float(price),
            "volume_usd_24h": float(vol24 or 0.0),
            "mentions": int(mentions or 0),
        })
    return out
