# Day 06 — Network Traffic Analyzer

**30 Days. 30 Challenges.**

This is Day 06 of the **30 Days of Cyber** community challenge. After focusing on file metadata and OPSEC in Day 05, today's project dives into the core of network security: Packet Sniffing and Traffic Analysis.

The goal: understand how data travels across a network, learn how to intercept it, and analyze the packets to extract valuable intelligence like Top Talkers, active ports, and DNS queries.

## What I Built

A Python-based **Network Traffic Analyzer** powered by the `scapy` library. 

This tool captures live network traffic on a specified interface, parses the raw packets, and generates a structured summary of the network activity. It identifies protocols (TCP/UDP/ICMP), tracks bandwidth usage, extracts requested DNS domains, and allows exporting the capture to a `.pcap` file for further deep-dive analysis in Wireshark.

## How It Works

Because network sniffing requires interacting directly with network interface cards (promiscuous mode), this script requires Administrator/Root privileges.

### 1. Installation
Install the required dependency (`scapy`) in your virtual environment:

    pip install scapy

*(Note for Windows users: You must install Npcap from the official Nmap website for packet capture to work).*

### 2. Running the Tool (Linux/Ubuntu)
To run the script with root privileges while maintaining the virtual environment context, use the following command:

    sudo $(which python) analyser.py

### Output Example:

    NETWORK TRAFFIC ANALYZER
    
    Available interfaces:
      1. eth0
      2. wlan0
      3. lo
    Pick interface (1-3) or Enter for all: 1
    Sniffing on: eth0
    How many packets to capture: 50
    Enter BPF filter (or press Enter for none): port 443 or port 53
    Capturing 50 packets...
    Captured 50 packets
    
    --- Protocol Breakdown ---
      TCP:   42
      UDP:   8
      ICMP:  0
      Other: 0
    
    --- Top Source IPs ---
      192.168.1.15: 28 packets
      104.18.32.47: 14 packets
    
    --- Top Destination Ports ---
      Port 443 [HTTPS]: 42 packets
      Port 53 [DNS]: 8 packets
    
    --- DNS Queries (domains being resolved) ---
      api.github.com
      raw.githubusercontent.com

## The Architecture & Features

### 1. Berkeley Packet Filter (BPF) Integration
The tool allows users to apply BPF syntax (e.g., `tcp and port 80`) directly before sniffing. This filters the noise at the kernel level, ensuring the script only processes relevant traffic and saving memory during large captures.

### 2. DNS Query Extraction (OSINT/Recon)
One of the most revealing parts of network traffic is DNS. Even if the subsequent HTTP traffic is encrypted (HTTPS), the initial DNS query is often transmitted in plaintext. The analyzer specifically dissects the `DNSQR` layer to reveal exactly which websites and APIs the host is communicating with.

### 3. PCAP Export
An analyzer is only as good as its logging. The tool uses `wrpcap` to dump the raw captured packets into a standard `.pcap` format, bridging the gap between this custom CLI tool and industry-standard GUI tools like Wireshark.

### 4. Anti-Crash & Error Handling
Network packets can be malformed, corrupted, or use unexpected encodings. The script implements safe decoding (`.decode('utf-8', 'ignore')`) and `haslayer()` checks to ensure that unexpected binary data doesn't crash the analysis loop.

## Project Structure

    network_traffic_analyzer/
    ├── analyser.py      # Core sniffing and analysis script
    └── README.md                # This file

## What I Learned

* **Scapy Layers:** Understanding how Scapy stacks network layers (`Ether / IP / TCP / Payload`) and how to navigate them programmatically.
* **Privilege Execution:** Learning the intricacies of running Python scripts with `sudo` while keeping the context of a local virtual environment (`$(which python)` trick).
* **Network Visibility:** Seeing firsthand how much intelligence can be gathered just by passively listening to a network interface, highlighting the absolute necessity of end-to-end encryption.

***
*#30DaysOfCyber*