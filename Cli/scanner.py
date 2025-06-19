# scanner.py
import os
import importlib
import requests
from urllib.parse import urlparse
from colorama import Fore, init

init(autoreset=True)

def validate_url(url):
    if not url.startswith("http"):
        url = "http://" + url
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(Fore.GREEN + "[+] Target is reachable.")
        else:
            print(Fore.YELLOW + f"[!] Status code: {response.status_code}")
        return url
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"[!] Error reaching target: {e}")
        return None

def load_modules():
    print(Fore.CYAN + "\n[*] Loading modules from /modules...\n")
    modules_dir = 'modules'
    for file in os.listdir(modules_dir):
        if file.endswith(".py") and not file.startswith("__"):
            module_name = file[:-3]
            full_module = f"modules.{module_name}"
            try:
                mod = importlib.import_module(full_module)
                print(Fore.YELLOW + f"[+] Running module: {module_name}")
                mod.run(validated_url)
            except Exception as e:
                print(Fore.RED + f"[!] Failed to run {module_name}: {e}")

if __name__ == "__main__":
    target = input(Fore.CYAN + "Enter target URL (with parameters): ").strip()
    validated_url = validate_url(target)
    if validated_url:
        print(Fore.CYAN + "[*] Starting full scan on:", validated_url)
        load_modules()
