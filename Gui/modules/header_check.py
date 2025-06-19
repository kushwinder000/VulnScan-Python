import requests

RECOMMENDED_HEADERS = {
    "Content-Security-Policy": "Prevents XSS and data injection attacks",
    "Strict-Transport-Security": "Forces secure (HTTPS) connections",
    "X-Content-Type-Options": "Prevents MIME-type sniffing",
    "X-Frame-Options": "Protects against clickjacking",
    "Referrer-Policy": "Controls referrer info sent with requests",
    "Permissions-Policy": "Restricts browser features",
    "X-XSS-Protection": "Basic XSS filter (deprecated but sometimes still checked)"
}

def run(url, log):
    log("[*] Checking for Security Headers...")

    try:
        response = requests.get(url, timeout=5)
        headers = response.headers

        for header, description in RECOMMENDED_HEADERS.items():
            if header in headers:
                log(f"[+] {header} → Present ✅")
            else:
                log(f"[!] {header} → Missing ❌")
                log(f"    ↪ Recommended: {description}")

    except Exception as e:
        log(f"[!] Failed to fetch headers: {e}")
