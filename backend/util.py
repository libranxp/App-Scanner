import datetime
import pytz
import logging

# Set up logging
logging.basicConfig(
    filename="scanner.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_trigger(ticker, reason, score):
    msg = f"Triggered: {ticker} | Reason: {reason} | Score: {score}"
    logging.info(msg)
    print(msg)  # Optional: for console visibility

def get_timestamp():
    tz = pytz.timezone("Europe/London")
    return datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

def format_price(value):
    return f"${value:.2f}"

def percent_change(old, new):
    try:
        return round(((new - old) / old) * 100, 2)
    except ZeroDivisionError:
        return 0.0
