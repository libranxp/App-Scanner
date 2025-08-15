import requests
import os

COINMARKETCAL_KEY = os.environ.get("COINMARKETCAL_KEY")

def get_crypto_events(page=1):
    url = f"https://developers.coinmarketcal.com/v1/events?access_token={COINMARKETCAL_KEY}&page={page}"
    return requests.get(url).json()
