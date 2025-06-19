# cli_version/modules/dir_listing.py
import requests
from urllib.parse import urlparse, urljoin
from colorama import Fore

def run(url):
    print(Fore.CYAN + "\n[*] Checking for Directory Listing...")

    try:
        parsed = urlparse(url)
        base = f"{parsed.scheme}://{parsed.netloc}"
        common_dirs = ["/admin/", "/backup/", "/uploads/", "/files/", "/logs/", "/images/", "/public/"]

        for dir in common_dirs:
            test_url = urljoin(base, dir)
            response = requests.get(test_url, timeout=5)
            content = response.text.lower()

            if "index of" in content and response.status_code == 200:
                print(Fore.RED + f"[!] Directory listing enabled at: {test_url}")
            elif response.status_code in [403, 401]:
                print(Fore.GREEN + f"[+] Directory listing blocked: {test_url} (Status {response.status_code})")
            else:
                print(Fore.YELLOW + f"[-] {test_url} (Status {response.status_code})")

    except Exception as e:
        print(Fore.RED + f"[!] Error checking directory listing: {e}")
