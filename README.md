# 🔍 VulnScan – Lightweight Website Vulnerability Scanner

**VulnScan** is a lightweight and modular Python-based website vulnerability scanner built for students, security enthusiasts, and ethical hackers. This tool scans websites for common vulnerabilities using both a command-line interface (CLI) and a graphical user interface (GUI) built with PyQt6.

---

## 🚀 Features

- ✅ SQL Injection Detection
- ✅ Cross-Site Scripting (XSS)
- ✅ Directory Listing Scanner
- ✅ Security Headers Check
- 🖥️ CLI and GUI support

---

## 📁 Project Structure

```plaintext
VulnScan/
├── cli/
│   └── vulnscan_cli.py
│   └── modules/
│       ├── sql_injection.py
│       ├── xss.py
│       ├── dir_listing.py
│       └── security_headers.py
│
├── gui/
│   └── main.py
│   └── modules/
│       ├── sql_module.py
│       ├── xss_module.py
│       ├── dir_module.py
│       └── headers_module.py
│
├── requirements.txt
├── README.md
```

---

## ⚙️ Requirements

```bash
pip install -r requirements.txt
```

---

## 🔧 How to Use

### ▶️ Run CLI Version
```bash
cd cli
python vulnscan_cli.py --url http://example.com
```

### 🖥️ Run GUI Version
```bash
cd gui
python main.py
```

---

## 📄 Output

The tool provides printed results in CLI and result panels in the GUI interface. Vulnerabilities like SQL injection and open directory listings are flagged clearly for analysis.

---

## 🔐 Ethical Use Notice

> ⚠️ This tool is meant **strictly for educational and ethical testing** purposes. Do not scan any website without proper authorization.

---

## 📫 Author

Created by [Kushwinder Dadwal](https://www.linkedin.com/in/kushwinder-dadwal-a35465208)
