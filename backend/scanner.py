def run_scan():
    print("🔍 Fetching live stock data...")
    stocks = fmp.fetch_most_active()

    if not stocks:
        print("⚠️ No data fetched, saving empty dashboard instead")
        save_dashboard([])
        return  # don't raise error, just exit cleanly
