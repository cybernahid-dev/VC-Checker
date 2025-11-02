#!/usr/bin/env python3
"""
VC Checker v1.0 — Offline Heuristic Malware Detection Tool
Developer: @cybernahid-dev
License: MIT
Description:
    - Scans local files for suspicious indicators.
    - Uses entropy, hash, extension, and pattern analysis.
    - Works fully offline (no external API calls).
    - Educational purpose only.
"""

import os
import hashlib
import math
from collections import Counter
import json
import click
from tqdm import tqdm
from datetime import datetime

# === Config ===
THREAT_DB = os.path.expanduser("~/.vc_checker/threatdb.json")
os.makedirs(os.path.dirname(THREAT_DB), exist_ok=True)

# === Utility Functions ===
def sha256_of_file(path, block_size=65536):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(block_size), b""):
            h.update(block)
    return h.hexdigest()

def calc_entropy(data):
    if not data:
        return 0.0
    freq = Counter(data)
    probs = [v / len(data) for v in freq.values()]
    return -sum(p * math.log2(p) for p in probs)

def suspicious_patterns(data):
    import re
    text = data.decode("latin-1", errors="ignore").lower()
    patterns = [
        (r"powershell", "powershell-script"),
        (r"cmd\.exe", "cmd-execution"),
        (r"eval\(", "eval-function"),
        (r"base64", "base64-code"),
        (r"socket", "network-socket"),
        (r"exec\(", "exec-call"),
    ]
    found = []
    for pat, tag in patterns:
        if re.search(pat, text):
            found.append(tag)
    return found

def load_threat_db():
    if not os.path.exists(THREAT_DB):
        return {"bad_hashes": []}
    with open(THREAT_DB, "r") as f:
        return json.load(f)

def save_threat_db(db):
    os.makedirs(os.path.dirname(THREAT_DB), exist_ok=True)
    with open(THREAT_DB, "w") as f:
        json.dump(db, f, indent=2)

# === Core Scan ===
def scan_file(path, threat_db):
    result = {"path": path, "size": None, "sha256": None, "entropy": None, "flags": [], "score": 0}
    try:
        size = os.path.getsize(path)
        result["size"] = size
        result["sha256"] = sha256_of_file(path)
        with open(path, "rb") as f:
            data = f.read(8192)
        ent = calc_entropy(data)
        result["entropy"] = round(ent, 2)

        if result["sha256"] in threat_db.get("bad_hashes", []):
            result["flags"].append("known-malware")
            result["score"] += 100

        ext = os.path.splitext(path)[1].lower()
        if ext in [".exe", ".dll", ".bat", ".vbs", ".ps1", ".js", ".jar"]:
            result["flags"].append("suspicious-extension")
            result["score"] += 25

        if ent > 7.5:
            result["flags"].append("high-entropy")
            result["score"] += 40

        if size > 50 * 1024 * 1024:
            result["flags"].append("large-file")
            result["score"] += 5

        pats = suspicious_patterns(data)
        if pats:
            result["flags"].extend(pats)
            result["score"] += len(pats) * 10

    except Exception as e:
        result["flags"].append(f"error:{e}")

    return result

# === CLI ===
@click.command()
@click.argument("target", type=click.Path(exists=True))
@click.option("--report", "-r", help="Save report as JSON file")
def main(target, report):
    """Scan files or folders for suspicious activity (offline)."""
    threat_db = load_threat_db()
    results = []
    files = []

    if os.path.isdir(target):
        for root, dirs, fs in os.walk(target):
            for f in fs:
                files.append(os.path.join(root, f))
    else:
        files.append(target)

    print(f"🔍 Scanning {len(files)} files...\n")
    for f in tqdm(files, desc="Scanning", unit="file"):
        results.append(scan_file(f, threat_db))

    # Summary
    print("\n=== SCAN SUMMARY ===")
    suspicious = [r for r in results if r["score"] >= 40]
    print(f"Total Files: {len(results)}")
    print(f"Suspicious: {len(suspicious)}")
    print(f"Report Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    if report:
        with open(report, "w") as rf:
            json.dump(results, rf, indent=2)
        print(f"📄 Report saved: {report}")
    else:
        for r in suspicious[:10]:
            print(f"⚠️ {r['path']}  → Score: {r['score']}  Flags: {r['flags']}")

if __name__ == "__main__":
    main()
