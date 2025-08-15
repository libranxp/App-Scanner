from providers import newsapi, lunarcrush, santiment
from datetime import datetime, timedelta

def enrich_with_catalysts(symbol):
    """Add news, social volume, and crypto sentiment info."""
    news_data = newsapi.get_news(symbol)
    social_data = lunarcrush.get_lunarcrush_assets(symbol)
    sentiment_data = santiment.get_social_volume(symbol.lower())

    return {
        "symbol": symbol,
        "news": news_data.get("articles", [])[:5],  # top 5 news
        "lunarcrush": social_data.get("data", {}),
        "social_volume": sentiment_data.get("data", {})
    }

if __name__ == "__main__":
    example = enrich_with_catalysts("BTC")
    print(example)
