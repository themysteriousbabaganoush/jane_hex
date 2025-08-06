import hashlib
import os
import sys
import time
import base64
import re
from tqdm import tqdm
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

ASCII_ART = r"""
 🧙‍♀️   Jane Hex
 Make them • Break them • Know them

 Hellsing Academy - Tech Division:
 Mun & Hellsing did it!!!
"""

def choose_algorithm():
    algos = sorted(hashlib.algorithms_guaranteed) + ['base64']
    print("\nAvailable algorithms:")
    for algo in algos:
        print(f"- {algo}")
    algo = input("Choose algorithm (default=md5): ").strip().lower() or 'md5'
    if algo not in algos:
        print(f"{Fore.RED}❌ Unsupported algorithm '{algo}'. Using md5 instead.")
        algo = 'md5'
    return algo

def get_salt():
    return input("Optional: enter salt to prepend/append (leave blank for none): ").strip()

def list_wordlists():
    base_dir = '/usr/share/wordlists/'
    files = [f for f in os.listdir(base_dir) if os.path.isfile(os.path.join(base_dir, f))]
    print("\nAvailable wordlists:")
    for idx, f in enumerate(files):
        print(f"{idx+1}. {f}")
    return files

def apply_hash_or_base64(text, algo, salt):
    if algo == 'base64':
        data = f"{salt}{text}{salt}".encode('utf-8') if salt else text.encode('utf-8')
        return base64.b64encode(data).decode('utf-8')
    else:
        data = f"{salt}{text}{salt}".encode('utf-8') if salt else text.encode('utf-8')
        h = hashlib.new(algo)
        h.update(data)
        return h.hexdigest()

def save_and_show_results(results, mode, algo):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    out_file = f"{mode}_{algo}_{timestamp}.txt"
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(results))
    print(f"\n{Fore.GREEN}✅ Results saved to {out_file}")
    print(f"\n{Fore.CYAN}=== Results on screen ===")
    for line in results:
        print(f"{Fore.YELLOW}{line}")

def do_reverse(target_hashes, candidates, algo, salt):
    found = {}
    for word in tqdm(candidates, desc="Reversing", colour="magenta"):
        if algo == 'base64':
            data = f"{salt}{word}{salt}".encode('utf-8') if salt else word.encode('utf-8')
            result = base64.b64encode(data).decode('utf-8').lower()
        else:
            data = f"{salt}{word}{salt}".encode('utf-8') if salt else word.encode('utf-8')
            h = hashlib.new(algo)
            h.update(data)
            result = h.hexdigest().lower()
        if result in target_hashes:
            found[result] = word
    return [f"{h} : {found.get(h, '<NOT FOUND>')}" for h in target_hashes]

def detect_hash_type():
    hash_value = input("Enter hash to detect type: ").strip()
    length = len(hash_value)
    if re.fullmatch(r'[a-fA-F0-9]+', hash_value):
        if length == 32:
            print(f"{Fore.CYAN}Possibly: MD5")
        elif length == 40:
            print(f"{Fore.CYAN}Possibly: SHA1")
        elif length == 64:
            print(f"{Fore.CYAN}Possibly: SHA256")
        elif length == 128:
            print(f"{Fore.CYAN}Possibly: SHA512")
        else:
            print(f"{Fore.YELLOW}Unknown or non-standard length.")
    else:
        print(f"{Fore.YELLOW}Not a standard hex hash.")
    print(f"{Fore.CYAN}Length: {length}")

def reverse_manual_input(hash_list, algo, salt):
    print("\nChoose word input method:")
    print("a. Pick from system wordlists (/usr/share/wordlists/)")
    print("b. Provide custom wordlist path")
    print("c. Enter words manually")
    opt = input("Choose option: ").strip().lower()

    candidates = []
    if opt == 'a':
        files = list_wordlists()
        idx = int(input("Enter number of wordlist to use: ")) - 1
        chosen = os.path.join('/usr/share/wordlists/', files[idx])
        with open(chosen, 'r', encoding='utf-8', errors='ignore') as f:
            candidates = [line.strip() for line in f if line.strip()]
    elif opt == 'b':
        custom_path = input("Enter custom wordlist path: ").strip()
        if not os.path.isfile(custom_path):
            print(f"{Fore.RED}❌ File not found.")
            return
        with open(custom_path, 'r', encoding='utf-8', errors='ignore') as f:
            candidates = [line.strip() for line in f if line.strip()]
    elif opt == 'c':
        print("Enter possible original words (end with empty line):")
        while True:
            word = input()
            if not word.strip():
                break
            candidates.append(word.strip())
    else:
        print(f"{Fore.RED}❌ Invalid option.")
        return

    results = do_reverse(hash_list, candidates, algo, salt)
    save_and_show_results(results, "reverse", algo)

def reverse_from_file(hash_file, algo, salt):
    if not os.path.isfile(hash_file):
        print(f"{Fore.RED}❌ Hash file not found.")
        return
    with open(hash_file, 'r', encoding='utf-8') as f:
        hashes = [line.strip().lower() for line in f if line.strip()]

    print("\nChoose wordlist:")
    print("a. Pick from system wordlists (/usr/share/wordlists/)")
    print("b. Provide custom path")
    opt = input("Choose option: ").strip().lower()

    candidates = []
    if opt == 'a':
        files = list_wordlists()
        idx = int(input("Enter number of wordlist to use: ")) - 1
        chosen = os.path.join('/usr/share/wordlists/', files[idx])
        with open(chosen, 'r', encoding='utf-8', errors='ignore') as f:
            candidates = [line.strip() for line in f if line.strip()]
    elif opt == 'b':
        custom_path = input("Enter custom wordlist path: ").strip()
        if not os.path.isfile(custom_path):
            print(f"{Fore.RED}❌ File not found.")
            return
        with open(custom_path, 'r', encoding='utf-8', errors='ignore') as f:
            candidates = [line.strip() for line in f if line.strip()]
    else:
        print(f"{Fore.RED}❌ Invalid option.")
        return

    results = do_reverse(hashes, candidates, algo, salt)
    save_and_show_results(results, "reverse", algo)

def main_menu():
    print(f"\n{Fore.CYAN}=== 🛡 Jane Hex CLI 🛡 ===")
    print("1. Make hashes")
    print("2. Reverse hashes")
    print("3. Detect hash type")
    choice = input("Choose option: ").strip()

    if choice == '1':
        algo = choose_algorithm()
        salt = get_salt()
        print("a. Enter text manually")
        print("b. Upload file")
        mode = input("Choose option: ").strip().lower()
        if mode == 'a':
            print("Enter text lines to hash (end with empty line):")
            lines = []
            while True:
                text = input()
                if not text.strip():
                    break
                lines.append(text.strip())
            hashes = [f"{line} : {apply_hash_or_base64(line, algo, salt)}" for line in tqdm(lines, desc="Hashing", colour="cyan")]
            save_and_show_results(hashes, "hashes", algo)
        elif mode == 'b':
            filepath = input("Enter path to file: ").strip()
            if not os.path.isfile(filepath):
                print(f"{Fore.RED}❌ File not found.")
                return
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                lines = [line.strip() for line in f if line.strip()]
            hashes = [f"{line} : {apply_hash_or_base64(line, algo, salt)}" for line in tqdm(lines, desc="Hashing file lines", colour="cyan")]
            save_and_show_results(hashes, "hashes", algo)
        else:
            print(f"{Fore.RED}❌ Invalid option.")

    elif choice == '2':
        algo = choose_algorithm()
        salt = get_salt()
        print("a. Reverse manually entered hashes")
        print("b. Reverse hashes from file")
        mode = input("Choose option: ").strip().lower()
        if mode == 'a':
            print("Enter hashes to reverse (one per line, end with empty line):")
            hashes = []
            while True:
                h = input()
                if not h.strip():
                    break
                hashes.append(h.strip().lower())
            reverse_manual_input(hashes, algo, salt)
        elif mode == 'b':
            hash_file = input("Enter path to hash file: ").strip()
            reverse_from_file(hash_file, algo, salt)
        else:
            print(f"{Fore.RED}❌ Invalid option.")
    elif choice == '3':
        detect_hash_type()
    else:
        print(f"{Fore.RED}❌ Invalid option.")

if __name__ == "__main__":
    print(f"{Fore.MAGENTA}{ASCII_ART}")
    while True:
        main_menu()
        again = input(f"\n{Fore.YELLOW}Run again? (y/n): ").strip().lower()
        if again != 'y':
            break
    print(f"{Fore.CYAN}👋 Goodbye, Chairman Hellsing!")
