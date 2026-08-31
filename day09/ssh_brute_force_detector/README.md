# Day 09 — SSH Brute Force Detector

## 30 Days. 30 Challenges.

This is Day 09 of the **30 Days of Cyber** community challenge — 30 days, 30 hands-on cybersecurity projects, built from scratch. Each day connects to the ones before it, starting from the basics and climbing toward real offensive/defensive scenarios.

The goal: research, learn, understand, and build. No copy-pasting tutorials — just real problem-solving.

---

## What I Built

A defensive security tool that continuously monitors system authentication logs for SSH brute-force attack patterns. It acts as an automated guard, detecting repeated failed login attempts, dynamically updating firewall rules to block malicious IPs, and maintaining professional audit trails. 

This project replicates the core mechanics of production-grade tools like Fail2Ban.

---

## How It Works

Run `sudo python3 main.py` to start the daemon. The tool reads `/var/log/auth.log` in real-time. If an IP fails to authenticate 5 times within a 10-minute window, the script executes an `iptables` command to drop all traffic from that IP. After 24 hours, the tool automatically lifts the ban.

**CRITICAL: The Whitelist**
Before running the tool, you **must** configure the whitelist to avoid locking yourself out of your own server.
Create a `whitelist.txt` file in the same directory and add trusted IP addresses (one per line). 
*Example:*
127.0.0.1
192.168.1.50
10.0.0.5

The script loads this file at startup. If an IP is on this list, it triggers an "early exit" in the code, completely bypassing the penalty tracking.

---

## The Core Mechanics Explained

### 1. State Tracking & Continuous Monitoring
To prevent memory exhaustion, the tool doesn't read the whole log file every time. 
**How it works:**
- It uses `f.seek(0, os.SEEK_END)` to jump to the end of the file, acting like the Linux `tail -f` command.
- It saves its exact byte position in a `bookmark.txt` file using `f.tell()`. If the script crashes or restarts, it resumes reading exactly where it left off so no attacks are missed.
- It monitors file size. If the size suddenly drops, it detects a **log rotation** (Linux archiving logs at midnight) and automatically resets its pointer to 0 to read the new file.

### 2. Threat Pattern Detection (Time-Windowing)
A single typo shouldn't result in a ban. The tool differentiates between human error and brute-force bots.
**How it works:**
- Uses a Python dictionary mapping attacker IPs to a list of timestamps (`time.time()`).
- On every failed attempt, it cleans up the list by removing timestamps older than 600 seconds (10 minutes).
- If the remaining length of the list is `>= 5`, the threshold is crossed and the attack is confirmed.

### 3. Firewall Automation & Auto-Unban
Once an attack is confirmed, the tool communicates directly with the Linux kernel's firewall.
**How it works:**
- **Block:** Uses Python's `subprocess` to execute `iptables -A INPUT -s <IP> -j DROP`.
- **Auto-Unban:** While waiting for new log lines, the script iterates through a dictionary of blocked IPs. If the current time minus the ban time is greater than 86,400 seconds (24 hours), it executes `iptables -D` to remove the rule and give the IP a second chance.

### 4. Professional Logging (Audit Trail)
Security tools must leave a paper trail. Instead of relying on `print()` statements that disappear when the terminal closes, this tool uses Python's `logging` module to maintain a persistent `ssh_bf_detector.log` file, recording every ban, unban, and error with exact timestamps.

---

## Security Best Practice: Keys vs. Passwords

While this tool effectively mitigates automated brute-force attacks, the ultimate defense against SSH brute-forcing is to **disable password authentication entirely**.

By configuring `/etc/ssh/sshd_config` with `PasswordAuthentication no`, you force the use of **SSH Keys** (Asymmetric Cryptography like RSA or Ed25519). A brute-force bot attempting to guess a 4096-bit cryptographic key is mathematically impossible. Fail2Ban and custom scripts like this one are great defense-in-depth mechanisms, but cryptographic keys eliminate the vulnerability at its root.

---

## Project Structure

ssh_brute_force_detector/
├── main.py                 # Main monitoring, detection, and blocking logic
├── whitelist.txt           # User-defined list of protected IPs (MUST BE CONFIGURED)
├── bookmark.txt            # Auto-generated state tracking memory file
├── ssh_bf_detector.log     # Persistent audit trail of security events
└── README.md               # This file

---

## What I Learned

- Reading files in real-time without memory exhaustion (`seek()`, `tell()`, `readline()`).
- Handling system edge cases like Linux log rotation.
- Managing system-level firewalls (`iptables`) programmatically via Python `subprocess`.
- Time-series tracking using dictionaries and list comprehensions.
- Applying the **"Early Exit" (Fail Fast)** software pattern for performance optimization (Whitelisting).
- Using Python `sets` for `O(1)` instant lookups.
- Creating professional audit trails using Python's `logging` module.

---

**#30DaysOfCyber**
