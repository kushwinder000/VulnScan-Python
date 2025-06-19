import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

sql_payloads = ["'", "\"", "'--", "\"--", "' OR '1'='1", "\" OR \"1\"=\"1"]

error_signatures = [
    "You have an error in your SQL syntax",
    "Warning: mysql_",
    "Unclosed quotation mark after the character string",
    "quoted string not properly terminated",
    "SQLSTATE"
]

def run(url, log):
    log("[*] Testing for SQL Injection...")
    vulnerable = False
    parsed = urlparse(url)
    queries = parse_qs(parsed.query)

    if not queries:
        log("[!] No query parameters to test for SQL injection.")
        return

    for param in queries:
        for payload in sql_payloads:
            temp_queries = queries.copy()
            temp_queries[param] = temp_queries[param][0] + payload
            new_query = urlencode(temp_queries, doseq=True)
            test_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', new_query, ''))

            try:
                response = requests.get(test_url, timeout=5)
                for error in error_signatures:
                    if error.lower() in response.text.lower():
                        log(f"[!] SQL Injection vulnerability detected with param '{param}' using payload '{payload}'")
                        log(f"    -> {test_url}")
                        vulnerable = True
                        break
            except Exception as e:
                log(f"[!] Request failed: {e}")

    if not vulnerable:
        log("[+] No SQL Injection vulnerabilities found.")
