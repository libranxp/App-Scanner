def update_dashboard(data):
    """Write fresh stock data to dashboard.json for frontend to load."""
    with open("dashboard.json", "w") as f:
        json.dump(data, f, indent=2)
