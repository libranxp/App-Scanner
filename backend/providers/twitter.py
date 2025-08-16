import os
import requests

BEARER = os.getenv("TWITTER_BEARER_TOKEN")

def fetch_tweets(query="stocks", max_results=10):
    url = "https://api.twitter.com/2/tweets/search/recent"
    headers = {"Authorization": f"Bearer {BEARER}"}
    r = requests.get(url, headers=headers, params={"query": query, "max_results": max_results})
    return r.json().get("data", []) if r.status_code == 200 else []
