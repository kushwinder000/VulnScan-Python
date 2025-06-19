import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

xss_payloads = [
    "<script>alert('XSS')</script>",
    "'\"><script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>",
]

def run(url, log):
    log("[*] Testing for XSS vulnerabilities...")
    vulnerable = False
    parsed = urlparse(url)
    queries = parse_qs(parsed.query)

    if not queries:
        log("[!] No query parameters to test for XSS.")
        return

    for param in queries:
        for payload in xss_payloads:
            temp_queries = queries.copy()
            temp_queries[param] = temp_queries[param][0] + payload
            new_query = urlencode(temp_queries, doseq=True)
            test_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', new_query, ''))

            try:
                response = requests.get(test_url, timeout=5)
                if payload.lower() in response.text.lower():
                    log(f"[!] Possible XSS vulnerability detected with param '{param}' using payload '{payload}'")
                    log(f"    -> {test_url}")
                    vulnerable = True
                    break
            except Exception as e:
                log(f"[!] Request failed: {e}")

    if not vulnerable:
        log("[+] No XSS vulnerabilities found.")
