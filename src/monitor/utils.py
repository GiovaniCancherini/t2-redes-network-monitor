from datetime import datetime

def now():
    return datetime.now().isoformat()

def timestamped_filename(prefix, ext):
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"{prefix}_{ts}.{ext}"