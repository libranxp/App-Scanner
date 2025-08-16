import requests

BASE = "https://www.reddit.com/r/wallstreetbets/new.json"

def fetch_reddit_posts(limit=10):
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(BASE, headers=headers, params={"limit": limit})
    if r.status_code == 200:
        return [p["data"]["title"] for p in r.json()["data"]["children"]]
    return []
