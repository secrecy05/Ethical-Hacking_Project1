# reporter.py
import json
import os
from datetime import datetime

SCANS_DIR = "scans"
os.makedirs(SCANS_DIR, exist_ok=True)

def save_scan(base_url, findings):
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    filename = f"{SCANS_DIR}/scan_{ts}.json"
    payload = {"base_url": base_url, "timestamp": ts, "findings": findings}
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    return filename

def load_scans():
    files = sorted([f for f in os.listdir(SCANS_DIR) if f.endswith(".json")], reverse=True)
    scans = []
    for fname in files:
        with open(os.path.join(SCANS_DIR, fname), "r", encoding="utf-8") as f:
            scans.append(json.load(f))
    return scans
