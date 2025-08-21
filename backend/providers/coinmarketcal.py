# backend/providers/coinmarketcal.py
import os, requests

API = os.getenv("COINMARKETCAL_API_KEY")

def catalysts_for_symbol(symbol: str, limit: int = 3):
    """
    Best-effort: fetch events mentioning the symbol.
    """
    url = "https://developers.coinmarketcal.com/v1/events"
    headers = {"x-api-key": API}
    params = {"max": limit, "coins": symbol}
    try:
        r = requests.get(url, headers=headers, params=params, timeout=30)
        r.raise_for_status()
        j = r.json()
        out = []
        for ev in j.get("body", []):
            out.append({
                "title": ev.get("title", "Event"),
                "source": ev.get("source") or ev.get("proof") or "",
                "url": ev.get("source") or ev.get("proof") or "",
            })
        return out
    except Exception as e:
        print(f"⚠️ CoinMarketCal error for {symbol}: {e}")
        return []
