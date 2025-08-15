import requests
import os

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY", "d1kopm1r01qt8fopliu0d1kopm1r01qt8fopliug")

def get_stock_quote(symbol):
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_API_KEY}"
    r = requests.get(url)
    return r.json()

def get_company_news(symbol, _from, to):
    url = f"https://finnhub.io/api/v1/company-news?symbol={symbol}&from={_from}&to={to}&token={FINNHUB_API_KEY}"
    r = requests.get(url)
    return r.json()
