import os, time, json, math, pytz, datetime as dt


LONDON = pytz.timezone('Europe/London')


def getenv(key, default=None):
v = os.environ.get(key, default)
return v


def now_london():
return dt.datetime.now(LONDON)


def within_bst_window():
t = now_london().time()
start = dt.time(8, 0)
end = dt.time(21, 0)
return start <= t <= end


def gate_45min(now=None):
n = now or now_london()
# Allow runs only when minute ∈ {00, 45}
return n.minute in (0, 45)


def retry(fn, attempts=3, delay=1.5):
last = None
for i in range(attempts):
try:
return fn()
except Exception as e:
last = e
time.sleep(delay * (i+1))
if last:
raise last


# JSON IO for Pages artifacts
DATA_DIR = os.path.join('docs', 'data')


def write_json(name, obj):
os.makedirs(DATA_DIR, exist_ok=True)
path = os.path.join(DATA_DIR, name)
with open(path, 'w') as f:
json.dump(obj, f, ensure_ascii=False, indent=2)
return path


def read_json(name, default=None):
path = os.path.join(DATA_DIR, name)
if not os.path.exists(path):
return default
with open(path, 'r') as f:
return json.load(f)
