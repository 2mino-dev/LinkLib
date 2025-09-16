import json
import os
import random
import requests
import string
from colorama import init, Fore, Style

init(autoreset=True) 

logo = r'''

     /$$       /$$           /$$       /$$       /$$ /$$              /$$$$$$  /$$ /$$
    | $$      |__/          | $$      | $$      |__/| $$             /$$__  $$| $$|__/
    | $$       /$$ /$$$$$$$ | $$   /$$| $$       /$$| $$$$$$$       | $$  \__/| $$ /$$
    | $$      | $$| $$__  $$| $$  /$$/| $$      | $$| $$__  $$      | $$      | $$| $$
    | $$      | $$| $$  \ $$| $$$$$$/ | $$      | $$| $$  \ $$      | $$      | $$| $$
    | $$      | $$| $$  | $$| $$_  $$ | $$      | $$| $$  | $$      | $$    $$| $$| $$
    | $$$$$$$$| $$| $$  | $$| $$ \  $$| $$$$$$$$| $$| $$$$$$$/      |  $$$$$$/| $$| $$
    |________/|__/|__/  |__/|__/  \__/|________/|__/|_______/        \______/ |__/|__/  

                            by 2mino-dev - version 1.0
                        < please star the repo on github >
                                                                      
'''
DB_FILE = "links.json"
#################################################
def load_data():
    if not os.path.exists(DB_FILE) or os.path.getsize(DB_FILE) == 0:
        print(Fore.YELLOW + "No links yet")
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)
    
def clear_data():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print(Fore.GREEN + "All links cleared")
    else:
        print(Fore.YELLOW + "already empty")

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=3)
        print(Fore.GREEN + "Links saved")

#################################################

def generate_key(length=6):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def check_data():
    if not os.path.exists(DB_FILE) or os.path.getsize(DB_FILE) == 0:
        
        with open(DB_FILE, "w") as f:
            json.dump({}, f, indent=2)
            print(Fore.YELLOW + "New file created")
        return {}  



def check_website(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(Fore.GREEN + "Website is reachable")
        else:
            print(Fore.RED + f"Website returned status code {response.status_code}")
    except requests.exceptions.RequestException:
         print(Fore.RED + "Error: Unable to reach the website")


def add_url(url):
    if not (url.startswith("http://") or url.startswith("https://")):
        print(Fore.RED + "Error: URL must start with http:// or https://")
        return
    
    if not check_website(url):
        print(Fore.YELLOW + "Adding link anyway...")
    
    data = load_data()
    key = generate_key()
    data[key] = url
    save_data(data)
    print(Fore.GREEN + f"Short link created: {key}")

def list_urls():
    data = load_data()
    if not data:
        print(Fore.YELLOW + "list: No links yet")
    else:
        print(Fore.CYAN + "Saved links:")
        for k, v in data.items():
            print(Fore.MAGENTA + f"{k}" + Fore.WHITE + " -> " + Fore.GREEN + f"{v}")


##################################################################################

def help_menu():
    print(Fore.CYAN + "Available commands:")
    print(Fore.YELLOW + " add <url>" + Fore.WHITE + " - Add a new URL to shorten")
    print(Fore.YELLOW + " list" + Fore.WHITE + " - List all saved URLs")
    print(Fore.YELLOW + " clear" + Fore.WHITE + " - Clear all saved URLs")
    print(Fore.YELLOW + " refresh" + Fore.WHITE + " - Refresh the screen")
    print(Fore.YELLOW + " exit" + Fore.WHITE + " - Exit the application")
    check_data()

def refresh_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    check_data()


def main():
    print(Fore.CYAN + logo)
    while True:
        cmd = input(Fore.BLUE + "LinkLib >> " + Style.RESET_ALL).strip().split()

        if not cmd:
            continue
        if cmd[0] == "exit":
            print(Fore.CYAN + "Bye Bye...")
            break
        elif cmd[0] == "add" and len(cmd) > 1:
            add_url(cmd[1])
        elif cmd[0] == "list":
            list_urls()
        elif cmd[0] == "clear":
            clear_data()
        elif cmd[0] == "refresh":
            refresh_screen()
            print(Fore.CYAN + logo)
        elif cmd[0] == "help":
            help_menu()
            
        else:
            print(Fore.RED + " Unknown command. Try: add <url>, list, exit")
check_data()


main()