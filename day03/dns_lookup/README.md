# Day 03 — DNS Reconnaissance Tool

**30 Days. 30 Challenges.**

This is Day 03 of the **30 Days of Cyber** community challenge — 30 days, 30 hands-on cybersecurity projects, built from scratch. After exploring port scanning in Day 02, today's project dives into **OSINT and Information Gathering** — specifically, mapping an organization's digital footprint through DNS Enumeration.

The goal: research, learn, understand, and build. No copy-pasting tutorials — just real problem-solving.

## What I Built

A robust, interactive **DNS Reconnaissance CLI Tool** written in Python. 

While simple `ping` commands give you an IP address, true reconnaissance requires extracting the hidden infrastructure of a target. This tool systematically queries multiple DNS record types (A, AAAA, MX, NS, TXT, CNAME) to reveal mail servers, third-party integrations, hosting providers, and security configurations (like SPF/DMARC). It also features a Reverse DNS engine to translate unknown IP addresses back to their hostnames.

## How It Works

Run the main Python script to launch the interactive menu. You can choose to perform a full domain footprinting or a reverse IP lookup.

```bash
# Install dependencies
pip install -r requirements.txt

# Run the tool
python main.py
```

### Output example:

```text
------------------------------
      DNS-LOOKUP TOOL      
------------------------------
1. Domain lookup
2. Reverse lookup (Ip to Hostname)
Pick (1 or 2): 1
Enter domain: github.com

==============================
DNS Lookup for github.com
==============================
 A Record: 140.82.113.3
 AAAA Record: No 'AAAA' record found.
 MX Record: aspmx.l.google.com. (Priority: 1)
 NS Record: ns1.p16.dynect.net.
 TXT Record: v=spf1 include:_spf.google.com ~all
==============================
```

## The Architecture Explained

### 1. The DRY Principle (Centralized Query Engine)
Initially, writing separate functions for every DNS record type resulted in massive code duplication (repeating the same `try/except` error handling blocks 6 times). To solve this, I implemented a centralized `_fetch_record` function. This single engine dynamically handles the specific parsing required for different records while managing all network exceptions in one place.

### 2. Smart Domain Validation (Pre-flight Checks)
A common issue with DNS scanners is terminal spam: if a user types a non-existent domain, the script throws 6 consecutive `NXDOMAIN` errors. 
To fix this, I engineered a `check_domain_exists` function. It attempts to resolve the `SOA` (Start of Authority) record first. If it fails, the script safely aborts the entire scan, providing a single, clean error message.

### 3. Record-Specific Parsing & Decoding
DNS records don't all return simple strings:
*   **TXT Records:** Stored as raw byte-strings that can easily break terminal formatting. The tool safely merges and decodes them into clean UTF-8 strings.
*   **MX Records:** The tool automatically extracts and formats both the server exchange and its priority (preference), vital for understanding mail routing.
*   **CNAME & NS Records:** Extracted using the specific `target` attributes from the `dnspython` library objects.

### 4. Reverse DNS Translation (PTR)
You cannot directly query an IP address in the DNS system. For the Reverse Lookup feature, the tool mathematically reverses the IP octets and appends the `.in-addr.arpa.` suffix before querying the `PTR` (Pointer) records to find the hidden hostname behind an IP.

## Project Structure

```text
dns-recon-tool/
├── requirements.txt      # Python dependencies (dnspython)
├── main.py               # Entry point (CLI interface & Validation)
├── dns_lookup.py         # Core logic (Centralized Query Engine)
└── README.md             # This file
```

## What I Learned

*   **DNS Fundamentals:** Deep dive into how A, AAAA, MX, NS, TXT, CNAME, and PTR records orchestrate the internet.
*   **Software Architecture:** Decoupling the User Interface (`main.py`) from the Business Logic (`dns_lookup.py`) and strictly applying the DRY principle.
*   **Exception Handling:** Managing granular network errors in Python (`NXDOMAIN`, `NoAnswer`, `Timeout`) to keep the application stable.
*   **Reconnaissance Methodology:** Learning how TXT records expose a company's internal tech stack (Microsoft 365, Docusign, Apple Pay, etc.) and email security policies.

***
*#30DaysOfCyber*