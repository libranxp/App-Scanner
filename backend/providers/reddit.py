import requests
import os

REDDIT_KEY = os.environ.get("REDDIT_KEY")

def get_subreddit_posts(subreddit):
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {"User-Agent": "Mozilla/5.0"}
    return requests.get(url, headers=headers).json()
