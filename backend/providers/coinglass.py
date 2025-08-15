import requests

def get_futures_open_interest():
    url = "https://open-api.coinglass.com/api/pro/v1/futures/openInterest"
    return requests.get(url).json()
