import requests
import os

POLYGON_API_KEY = os.environ.get("POLYGON_API_KEY")

def get_ticker_details(ticker):
    url = f"https://api.polygon.io/v3/reference/tickers/{ticker}?apiKey={POLYGON_API_KEY}"
    return requests.get(url).json()

def get_previous_close(ticker):
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/prev?apiKey={POLYGON_API_KEY}"
    return requests.get(url).json()
