import datetime

def log(msg, level='info'):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{now}] [{level.upper()}] {msg}")
