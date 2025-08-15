import requests
import os

NEWSAPI_KEY = os.environ.get("NEWSAPI_KEY")

def get_news(query):
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={NEWSAPI_KEY}"
    return requests.get(url).json()
