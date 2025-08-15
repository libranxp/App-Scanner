import requests
import os

FMP_API_KEY = os.getenv("FMP_API_KEY", "C3tvXXFVYcEg7VBI8ycZsUQrNDCGIGo8")

def get_stock_profile(symbol):
    url = f"https://financialmodelingprep.com/api/v3/profile/{symbol}?apikey={FMP_API_KEY}"
    return requests.get(url).json()

def get_market_gainers():
    url = f"https://financialmodelingprep.com/api/v3/stock/gainers?apikey={FMP_API_KEY}"
    return requests.get(url).json()
