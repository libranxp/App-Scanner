import requests

def get_massari_assets():
    url = "https://data.messari.io/api/v1/assets"
    return requests.get(url).json()
