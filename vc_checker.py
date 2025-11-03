#!/usr/bin/env python3
# VC Checker v1.1 (Auto Path Detect + Real-time Scan)
# Author: cybernahid-dev | 2025
# Educational local scanner

import os, re, sys, time
from datetime import datetime

BANNER = r"""
 /$$    /$$  /$$$$$$         /$$$$$$  /$$   /$$ /$$$$$$$$  /$$$$$$  /$$   /$$ /$$$$$$$$ /$$$$$$$       
| $$   | $$ /$$__  $$       /$$__  $$| $$  | $$| $$_____/ /$$__  $$| $$  /$$/| $$_____/| $$__  $$      
| $$   | $$| $$  \__/      | $$  \__/| $$  | $$| $$      | $$  \__/| $$ /$$/ | $$      | $$  \ $$      
|  $$ / $$/| $$            | $$      | $$$$$$$$| $$$$$   | $$      | $$$$$/  | $$$$$   | $$$$$$$/      
 \  $$ $$/ | $$            | $$      | $$__  $$| $$__/   | $$      | $$  $$  | $$__/   | $$__  $$      
  \  $$$/  | $$    $$      | $$    $$| $$  | $$| $$      | $$    $$| $$\  $$ | $$      | $$  \ $$      
   \  $/   |  $$$$$$/      |  $$$$$$/| $$  | $$| $$$$$$$$|  $$$$$$/| $$ \  $$| $$$$$$$$| $$  | $$      
    \_/     \______/        \______/ |__/  |__/|________/ \______/ |__/  \__/|________/|__/  |__/      

                      VC CHECKER  v1.1  |  by cybernahid-dev
"""

DISCLAIMER = """
⚠️ DISCLAIMER:
This tool is for cybersecurity learning purposes only.
It performs local text-based pattern scans (no system modification).
No scanner can guarantee 100% detection accuracy.
Always verify with multiple trusted tools.
"""

DEFAULT_SIGNATURES = [
    r"eval\s*\(",
    r"base64_decode\s*\(",
    r"exec\s*\(",
    r"subprocess\.Popen",
    r"import\s+os",
    r"(?i)password\s*[:=]",
    r"(?i)api[_-]?key",
    r"(?i)trojan",
    r"(?i)malware",
]

SEARCH_ROOTS = [
    ".",  # current directory
    os.path.expanduser("~"),
    "/sdcard",
    "/storage",
    "/data/data/com.termux/files/home"
]

def load_signatures():
    sigs = []
    if os.path.exists("signatures.txt"):
        with open("signatures.txt", "r", encoding="utf-8", errors="ignore") as fh:
            for ln in fh:
                ln = ln.strip()
                if ln and not ln.startswith("#"):
                    try:
                        sigs.append(re.compile(ln))
                    except re.error:
                        pass
    if not sigs:
        sigs = [re.compile(x) for x in DEFAULT_SIGNATURES]
    return sigs

def read_chunk(path, limit_bytes=1024*1024):
    try:
        with open(path, "rb") as f:
            data = f.read(limit_bytes)
        return data.decode("utf-8", errors="ignore")
    except Exception:
        return ""

def scan_file(path, signatures):
    text = read_chunk(path)
    matches = []
    for s in signatures:
        if s.search(text):
            matches.append(s.pattern)
    return matches

def scan_directory(target, signatures):
    total = 0
    infected = []
    start = time.time()
    print(f"\n🔍 Scanning: {target}\n{'-'*60}")
    for root, dirs, files in os.walk(target):
        for fname in files:
            total += 1
            path = os.path.join(root, fname)
            m = scan_file(path, signatures)
            if m:
                infected.append((path, m))
                print(f"⚠️  [{total}] Suspicious → {path}")
                for pat in m:
                    print(f"    → Matched: {pat}")
            else:
                print(f"✅ [{total}] {fname}")
    duration = round(time.time() - start, 2)
    print("\n" + "="*60)
    print(f"📁 Files Scanned : {total}")
    print(f"🚨 Threats Found : {len(infected)}")
    print(f"⏱️  Duration      : {duration}s")
    print("="*60)
    if infected:
        print("\n⚠️ Infected files:")
        for p, _ in infected:
            print(f" - {p}")
    else:
        print("\n✅ No threats detected!")
    print("\nScan complete.\n")

def find_paths_by_name(name, roots=SEARCH_ROOTS, max_results=10):
    found = []
    name = name.lower()
    for root in roots:
        if not os.path.exists(root):
            continue
        for dirpath, dirnames, _ in os.walk(root):
            base = os.path.basename(dirpath).lower()
            if name in base:
                found.append(dirpath)
                if len(found) >= max_results:
                    return found
    return found

def resolve_target(name):
    if os.path.exists(name):
        return os.path.abspath(name)
    print(f"\n🔎 Searching for '{name}' ...")
    matches = find_paths_by_name(name)
    if not matches:
        return None
    if len(matches) == 1:
        return matches[0]
    print("\nMultiple matches found:")
    for i, p in enumerate(matches, 1):
        print(f"[{i}] {p}")
    ch = input("Select (1-default): ").strip()
    if not ch:
        return matches[0]
    if ch.isdigit() and 1 <= int(ch) <= len(matches):
        return matches[int(ch) - 1]
    return matches[0]

def main():
    os.system("clear")
    print(BANNER)
    print(DISCLAIMER)
    sigs = load_signatures()

    if len(sys.argv) > 1:
        target_input = " ".join(sys.argv[1:]).strip()
    else:
        target_input = input("\nEnter folder or file name/path to scan: ").strip()

    if not target_input:
        print("❌ No input provided.")
        sys.exit(1)

    target = resolve_target(target_input)
    if not target:
        print(f"❌ No matching directories found for '{target_input}'")
        print("Tip: Try giving a full or existing folder name.")
        sys.exit(1)

    print(f"\n✅ Selected path: {target}")
    confirm = input("Proceed to scan? (Y/n): ").strip().lower()
    if confirm == "n":
        print("Cancelled.")
        sys.exit(0)

    scan_directory(target, sigs)

if __name__ == "__main__":
    main()
