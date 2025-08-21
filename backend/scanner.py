import json
import os

def save_dashboard(stocks):
    """Always save dashboard.json at repo root"""
    dashboard_path = os.path.join(os.path.dirname(__file__), "..", "dashboard.json")
    dashboard_path = os.path.abspath(dashboard_path)

    with open(dashboard_path, "w") as f:
        json.dump(stocks, f, indent=2)

    print(f"✅ Dashboard data saved to {dashboard_path}")
