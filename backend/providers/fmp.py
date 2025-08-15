import requests
import os

FMP_API_KEY = os.environ.get("FMP_API_KEY")

def get_stock_profile(symbol):
    url = f"https://financialmodelingprep.com/api/v3/profile/{symbol}?apikey={FMP_API_KEY}"
    return requests.get(url).json()

def get_market_gainers():
    url = f"https://financialmodelingprep.com/api/v3/stock/gainers?apikey={FMP_API_KEY}"
    return requests.get(url).json()
