import requests
import os

ALPHAVANTAGE_API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY")

def get_rsi(symbol, interval="daily", time_period=14):
    url = f"https://www.alphavantage.co/query?function=RSI&symbol={symbol}&interval={interval}&time_period={time_period}&series_type=close&apikey={ALPHAVANTAGE_API_KEY}"
    return requests.get(url).json()
