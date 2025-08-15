import os
import json
from datetime import datetime
import pytz

BST = pytz.timezone("Europe/London")

def load_json(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return {}

def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def current_time_str():
    return datetime.now(BST).strftime('%Y-%m-%d %H:%M:%S BST')
