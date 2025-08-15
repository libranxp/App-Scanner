import requests
import os

LUNARCRUSH_API_KEY = os.environ.get("LUNARCRUSH_API_KEY")

def get_lunarcrush_assets(symbol):
    url = f"https://api.lunarcrush.com/v2?data=assets&key={LUNARCRUSH_API_KEY}&symbol={symbol}"
    return requests.get(url).json()
