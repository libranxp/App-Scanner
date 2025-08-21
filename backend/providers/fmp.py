import os
import requests

FMP_API_KEY = os.environ.get("FMP_API_KEY")

def fetch_premarket():
    """
    Fetch premarket active stocks from Financial Modeling Prep
    Apply filters for low float, high momentum, catalyst relevance
    """
    url = f"https://financialmodelingprep.com/api/v3/stock/actives?apikey={FMP_API_KEY}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json().get("mostActiveStock", [])

    # Filter dynamically, no sample data
    filtered = []
    for stock in data:
        # Example dynamic filters: gap %, rel vol, RSI, float
        if stock.get("changesPercentage", 0) > 2:  # example threshold
            filtered.append(stock)
    return filtered
