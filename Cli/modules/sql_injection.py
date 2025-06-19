# cli_version/modules/sql_injection.py
import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from colorama import Fore

sql_payloads = ["'", "\"", "'--", "\"--", "' OR '1'='1", "\" OR \"1\"=\"1"]

error_signatures = [
    "You have an error in your SQL syntax",
    "Warning: mysql_",
    "Unclosed quotation mark after the character string",
    "quoted string not properly terminated",
    "SQLSTATE"
]

def run(url):
    print(Fore.CYAN + "\n[*] Testing for SQL Injection...")
    vulnerable = False
    parsed = urlparse(url)
    queries = parse_qs(parsed.query)

    if not queries:
        print(Fore.YELLOW + "[!] No query parameters to test for SQL injection.")
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
                        print(Fore.RED + f"[!] SQL Injection vulnerability detected with param '{param}' using payload '{payload}'")
                        print(Fore.RED + f"    -> {test_url}")
                        vulnerable = True
                        break
            except Exception as e:
                print(Fore.YELLOW + f"[!] Request failed: {e}")

    if not vulnerable:
        print(Fore.GREEN + "[+] No SQL Injection vulnerabilities found.")
