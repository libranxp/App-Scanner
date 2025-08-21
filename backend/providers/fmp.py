# backend/providers/fmp.py
import os, requests

API = os.getenv("FMP_API_KEY")

def fetch_most_active(limit: int = 50):
    """Live US most active list (no pre-picked tickers)."""
    url = f"https://financialmodelingprep.com/api/v3/stock/actives?apikey={API}"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    payload = r.json()
    items = payload.get("mostActiveStock", []) if isinstance(payload, dict) else payload
    out = []
    for it in items:
        sym = it.get("ticker") or it.get("symbol")
        if not sym: continue
        out.append({
            "symbol": sym.upper(),
            "price": float(it.get("price") or 0.0),
            "change_pct": float(str(it.get("changesPercentage", "0")).strip('%+ ')),
            "volume": float(it.get("volume") or 0.0),
        })
    return out[:limit]
