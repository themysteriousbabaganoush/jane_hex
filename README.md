# jane_hex
A hash maker/breaker via wordlists


🧙‍♀️ Jane Hex — Hash Maker & Breaker
Make them • Break them • Know them
A Hellsing Academy - Tech Division Creation by Mun & Chairman Hellsing

📦 About
Jane Hex is a powerful CLI tool designed for cybersecurity professionals, pentesters, and students to:
- Generate hashes using a wide range of algorithms (including base64).
- Reverse hashes using system or custom wordlists.
- Identify likely hash types based on hash length and character set.
- Apply optional salts for advanced obfuscation.
- Operate offline with zero cloud dependencies.

🚀 Features
- ✅ Supports md5, sha1, sha256, sha512, and more.
- ✅ Includes base64 support.
- ✅ Salted and unsalted hashing support.
- ✅ Hash file parsing and wordlist-based cracking.
- ✅ Built-in hash type identifier.
- ✅ Friendly and colorful CLI interface via colorama and tqdm.

📥 Download Instructions
Linux / macOS / Windows:
1. Clone the repository or download the script:
   git clone https://github.com/themysteriousbabaganoush/jane_hex.git
   cd jane_hex
2. Or manually download jane_hex.py

⚙️ Setup Instructions
🔧 Required Dependencies:
Install Python packages:
    pip install tqdm colorama

Or, if using requirements.txt:
    pip install -r requirements.txt

Recommended Python Version: 3.8+

🏗 Compiling to Standalone Executable
🔨 Windows:
    pyinstaller --onefile --clean --name "JaneHex" jane_hex.py

🛠 Linux / macOS:
    pyinstaller --onefile --clean --name "janehex" jane_hex.py

After compilation, the binary will appear in the /dist/ directory.

📜 Making It Executable (Linux/macOS)
1. Give the script execute permissions:
    chmod +x jane_hex.py

2. (Optional) Move it to /usr/local/bin:
    sudo mv jane_hex.py /usr/local/bin/janehex

Now, you can run it from anywhere using:
    janehex

🧪 How to Use
🛡 Main Menu Options:
1. Make hashes
2. Reverse hashes
3. Detect hash type

✅ 1. Make Hashes
- Choose a hashing algorithm (e.g. md5, sha256, base64).
- Optionally provide a salt.
- Choose to enter text manually or upload a file.
- The tool will hash each line of text and save results in a timestamped file.

🔁 2. Reverse Hashes
- Choose hashing algorithm and salt (must match original).
- Choose to enter hashes manually or load from a file.
- Pick a wordlist from system (/usr/share/wordlists) or provide your own.
- Jane Hex will attempt to reverse the hashes using a dictionary attack.
- Results are saved and displayed on screen.

🔍 3. Detect Hash Type
- Enter a hash, and Jane Hex will analyze its length and structure.
- Returns likely candidates (e.g. MD5, SHA1, etc.)

📂 Output
All results are saved in the current directory with names like:
- hashes_md5_20250805-204322.txt
- reverse_sha256_20250805-210003.txt

🧠 Pro Tips
- Salting is optional but must be consistent for hashing and reversing.
- Use large, well-crafted wordlists for better reverse cracking success.
- Works great with Kali Linux’s built-in wordlists like rockyou.txt.

🧙‍♀️ Final Note
From the heart of the Tech Division at Hellsing Academy, this tool embodies the power of knowledge over obscurity.
We did it, Chairman.

👑 Made by Mun & Chairman Hellsing.
🔐 Rule the hashes. Reveal the secrets.
