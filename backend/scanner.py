import os
import json

def save_dashboard(data, path="dashboard.json"):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Dashboard updated at {os.path.abspath(path)}")
