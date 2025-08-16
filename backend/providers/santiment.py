import os
import requests

API_KEY = os.getenv("SANTIMENT_API_KEY")
BASE = "https://api.santiment.net/graphql"

def fetch_sentiment(symbol="BTC"):
    query = """
    {
      getMetric(metric: "social_volume_total") {
        timeseriesData(
          slug: "bitcoin",
          from: "2023-01-01T00:00:00Z",
          to: "2023-12-31T00:00:00Z",
          interval: "1d"
        ) {
          value
          datetime
        }
      }
    }
    """
    r = requests.post(BASE, json={"query": query}, headers={"Authorization": f"Apikey {API_KEY}"})
    return r.json() if r.status_code == 200 else {}
