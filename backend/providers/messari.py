# backend/providers/messari.py
import os, requests

API = os.getenv("MESSARI_API_KEY")

def top_assets(limit: int = 50):
    url = "https://data.messari.io/api/v2/assets?fields=id,slug,symbol,metrics/market_data/price_usd,metrics/marketcap/current_marketcap_usd,metrics/market_data/real_volume_last_24_hours"
    headers = {"x-messari-api-key": API}
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    j = r.json()
    out = []
    for it in j.get("data", [])[:limit]:
        sym = (it.get("symbol") or "").upper()
        md = ((it.get("metrics") or {}).get("market_data") or {})
        price = md.get("price_usd")
        vol = md.get("real_volume_last_24_hours")
        mcap = ((it.get("metrics") or {}).get("marketcap") or {}).get("current_marketcap_usd")
        if not sym or price is None: continue
        out.append({
            "symbol": sym,
            "price": float(price),
            "volume_usd_24h": float(vol or 0.0),
            "market_cap": float(mcap or 0.0),
        })
    return out
