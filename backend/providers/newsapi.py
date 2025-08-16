import os
import requests

API_KEY = os.getenv("NEWSAPI_API_KEY")
BASE = "https://newsapi.org/v2/everything"

def fetch_news(query="stocks"):
    r = requests.get(BASE, params={"q": query, "apiKey": API_KEY, "pageSize": 10})
    return r.json().get("articles", []) if r.status_code == 200 else []
