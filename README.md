# 🧠 VC Checker v1.0 — Offline Heuristic Malware Detection Tool

**Developer:** @cybernahid-dev  
**License:** MIT  
**Purpose:** Educational & Research use for safe malware detection and cybersecurity learning.

---

## 🚀 Features
- 🧩 Offline — Works with no Internet connection or API keys  
- 🔍 Heuristic scanning (entropy, extension, code patterns)  
- 🧠 Detects suspicious PowerShell, Base64, obfuscated JS patterns  
- ⚙️ Local threat hash database (`~/.vc_checker/threatdb.json`)  
- 🧾 JSON report generation  
- 💻 Works on Termux, Linux, and Windows  

---

## ⚖️ Legal Disclaimer
VC Checker is strictly for **educational and ethical cybersecurity learning**.  
Do **not** use it to scan systems or files without authorization.  
The developer is **not responsible** for any misuse.

---

## 🧰 Installation

### For Termux / Linux

pkg install python git -y
git clone https://github.com/cybernahid-dev/VC-Checker.git
cd VC-Checker
pip install -r requirement.txt


## 🧠 Usage

Basic Scan

python vc_checker.py /path/to/folder

Save JSON Report

python vc_checker.py /path/to/files -r report.json

Example Output

=== SCAN SUMMARY ===
Total Files: 34
Suspicious: 2
Report Time: 2025-11-02 20:45:21
⚠️ /Downloads/test.exe → Score: 85  Flags: ['suspicious-extension', 'high-entropy']


---

## 🗂️ Local Threat DB (optional)

You can store known malicious hashes for offline matching:

mkdir -p ~/.vc_checker
echo '{"bad_hashes": ["abc123...sha256hash"]}' > ~/.vc_checker/threatdb.json


---

## 🧩 Future Roadmap

🔔 Real-time auto-scan mode

📈 YARA rule integration (optional)

🧠 ML-based behavior scoring (offline learning)

🌐 Optional VT lookup (user key)

🧰 GUI dashboard for Windows



---

## 🪪 License

This project is licensed under the MIT License.
© 2025 — Developed by @cybernahid-dev

# VC-Checker
