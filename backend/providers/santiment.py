import requests
import os

SANTIMENT_API_KEY = os.environ.get("SANTIMENT_API_KEY")

def get_social_volume(asset):
    url = f"https://api.santiment.net/graphql"
    headers = {"Authorization": f"Apikey {SANTIMENT_API_KEY}"}
    query = {
        "query": f'{{ getMetric(metric: "social_volume_total"){{ timeseriesData(slug: "{asset}", from: "2023-07-01T00:00:00Z", to: "2023-07-02T00:00:00Z"){{ datetime, value }} }} }}'
    }
    return requests.post(url, json=query, headers=headers).json()
