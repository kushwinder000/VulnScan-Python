import requests
from urllib.parse import urljoin

common_dirs = [
    "admin/",
    "backup/",
    "uploads/",
    "test/",
    "old/",
    "config/",
    "data/",
]

def run(url, log):
    log("[*] Checking for Directory Listing vulnerabilities...")
    vulnerable_dirs = []

    if not url.endswith('/'):
        url += '/'

    for directory in common_dirs:
        test_url = urljoin(url, directory)
        try:
            response = requests.get(test_url, timeout=5)
            if response.status_code == 200 and ("Index of /" in response.text or "Directory listing for" in response.text):
                log(f"[!] Directory listing enabled at: {test_url}")
                vulnerable_dirs.append(test_url)
        except Exception as e:
            log(f"[!] Request failed for {test_url}: {e}")

    if not vulnerable_dirs:
        log("[+] No directory listing vulnerabilities found.")
