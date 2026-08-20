# Day 04 — Hash Cracker Tool

**30 Days. 30 Challenges.**

This is Day 04 of the **30 Days of Cyber** community challenge — 30 days, 30 hands-on cybersecurity projects, built from scratch. After exploring OSINT and DNS enumeration in Day 03, today's project dives into **Cryptography and Offensive Security** — specifically, building an offline password cracking engine.

The goal: research, learn, understand, and build. No copy-pasting tutorials — just real problem-solving.

## What I Built

A robust, interactive **Hash Cracker CLI Tool** written in Python. 

While online tools exist, understanding how hashes are broken locally is fundamental to password security and auditing. This tool systematically attempts to crack hashes (MD5, SHA1, SHA256, SHA512) using four different attack vectors: standard Dictionary, pure Brute Force, Dictionary with Rules (mutations/leet speak), and a highly optimized Multiprocessing mode to maximize CPU utilization.

## How It Works

Run the main Python script to launch the interactive menu. You will need a wordlist (like `rockyou.txt`) for the dictionary modes.

```bash
# Run the tool
python main.py
```

### Output example:
```text
------------------------------
      HASH CRACKER TOOL      
------------------------------
1. Dictionary
2. Brute Force
3. Dictionary + rules
4. Dictionary (Multiprocess)
Pick (1, 2, 3 or 4): 4
Enter hash to crack: 5f4dcc3b5aa765d61d8327deb882cf99
Enter wordlist path: rockyou.txt

==============================
Cracking Hash: 5f4dcc3b5aa765d61d8327deb882cf99
Detected hash type: md5
==============================
CRACKED: password (in 1.24s)
==============================
```

## The Architecture Explained

### 1. Bypassing the Python GIL (Multiprocessing)
Hash cracking is purely mathematical (CPU-bound). Standard Python threads are limited by the Global Interpreter Lock (GIL), meaning they can only use one CPU core at a time. To solve this in Mode 4, I implemented Python's `multiprocessing` library. The tool splits the wordlist into chunks based on `cpu_count()` and spawns entirely separate processes. They communicate their success back to the main program using shared memory (`Value` and `Manager`).

### 2. Rule-Based Mutations
People rarely use completely random passwords; they use variations of known words. The `crack_rules` function takes a standard dictionary word and generates smart mutations on the fly (capitalization, appending numbers 0-9, and common leet speak replacements like `a` to `@` or `e` to `3`). This drastically increases the success rate without needing a multi-gigabyte wordlist.

### 3. Itertools for Brute Force
For the pure brute-force mode, generating every possible character combination efficiently is critical. I utilized Python's `itertools.product` to dynamically generate strings of increasing lengths based on a user-selected charset (lowercase, uppercase, digits, and symbols), ensuring zero memory bloat during generation.

### 4. Automatic Hash Detection
Instead of asking the user what type of hash they are inputting, the `detect_hash` function analyzes the length of the string (e.g., 32 characters for MD5, 64 for SHA256) to automatically route the cracking logic to the correct algorithm in the `hashlib` library.

## Project Structure

```text
hash_cracker/
├── main.py               # Entry point (CLI interface & User Input)
├── hash_cracker.py       # Core logic (Hashing, Mutations, Multiprocessing)
└── README.md             # This file
```

## What I Learned

* **Concurrency vs Parallelism:** Understanding the difference between I/O-bound tasks (where threads work well) and CPU-bound tasks (which require true Multiprocessing to bypass the GIL).
* **Memory Management:** Reading massive files like `rockyou.txt` securely using iterators (`for line in f:`) and the `latin-1` encoding to prevent `MemoryError` and `UnicodeDecodeError` crashes.
* **Cryptography Flaws:** Seeing firsthand why MD5 and SHA1 are considered obsolete for storing passwords due to how quickly modern CPUs can compute their hashes.
* **Shared State Execution:** Using `multiprocessing.Value` as a flag to safely stop all background processes the moment one of them finds the correct password.

***
*#30DaysOfCyber*