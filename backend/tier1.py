from providers import finnhub, fmp, polygon
from datetime import datetime, timedelta

def get_premarket_gainers():
    """Fetch top premarket stock gainers."""
    gainers = fmp.get_market_gainers()
    filtered = []

    for stock in gainers[:50]:  # top 50
        symbol = stock["ticker"]
        quote = finnhub.get_stock_quote(symbol)
        prev_close = polygon.get_previous_close(symbol)
        gap_percent = ((quote["c"] - prev_close["results"][0]["c"]) / prev_close["results"][0]["c"]) * 100
        if gap_percent > 2:  # filter for >2% premarket gap
            filtered.append({
                "symbol": symbol,
                "price": quote["c"],
                "gap": round(gap_percent, 2),
                "volume": quote["v"],
            })
    return filtered

if __name__ == "__main__":
    gainers = get_premarket_gainers()
    for g in gainers:
        print(g)
