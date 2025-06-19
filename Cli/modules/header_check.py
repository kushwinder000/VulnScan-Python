# cli_version/modules/header_check.py
import requests
from colorama import Fore

# Common security headers
RECOMMENDED_HEADERS = {
    "Content-Security-Policy": "Prevents XSS and data injection attacks",
    "Strict-Transport-Security": "Forces secure (HTTPS) connections",
    "X-Content-Type-Options": "Prevents MIME-type sniffing",
    "X-Frame-Options": "Protects against clickjacking",
    "Referrer-Policy": "Controls referrer info sent with requests",
    "Permissions-Policy": "Restricts browser features",
    "X-XSS-Protection": "Basic XSS filter (deprecated but sometimes still checked)"
}

def run(url):
    print(Fore.CYAN + "\n[*] Checking for Security Headers...")

    try:
        response = requests.get(url, timeout=5)
        headers = response.headers

        for header, description in RECOMMENDED_HEADERS.items():
            if header in headers:
                print(Fore.GREEN + f"[+] {header} → Present ✅")
            else:
                print(Fore.RED + f"[!] {header} → Missing ❌")
                print(Fore.YELLOW + f"    ↪ Recommended: {description}")

    except Exception as e:
        print(Fore.RED + f"[!] Failed to fetch headers: {e}")
