# Day 07 — Week 1 Retrospective & Review

**30 Days. 30 Challenges.**

Today is Day 07 of the **30 Days of Cyber** challenge. Instead of writing new code, today is dedicated to stepping back, reviewing the architecture of the tools built over the past six days, and consolidating the core concepts learned during Week 1.

## Week 1 Recap: Networking, Cryptography & Recon

The first week was heavily focused on understanding how data moves, how it's protected, and how it can be intercepted or analyzed. Moving between Python for rapid scripting and Go for high-performance concurrent networking provided a well-rounded foundation.

### The Arsenal Built So Far:
* **Multi-Cipher CLI Tool:** Explored cryptography fundamentals by manually implementing Base64, Caesar, Vigenère, and Hexadecimal encoding/decoding.
* **Concurrent TCP Port Scanner:** Dove into network sockets and leveraged Go's concurrency model (goroutines, worker pools, and channels) to build a high-speed scanner.
* **Network Intrusion Detection System (NIDS):** Built a custom Go-based engine capable of signature matching, payload analysis, and detecting reconnaissance techniques like ping sweeps.
* **Metadata Scrubber (OPSEC):** Created a Python utility to extract and destroy hidden EXIF and document metadata to prevent intelligence leaks.
* **Network Traffic Analyzer:** Used Scapy to passively sniff live packets, parse layers, and extract plaintext DNS queries for network reconnaissance.

## Key Takeaways

1. **Concurrency is King for Networking:** Building the port scanner and NIDS in Go highlighted how essential concurrent design is for creating efficient security tools that don't bottleneck.
2. **Nothing is Truly Hidden:** The metadata scrubber and traffic analyzer proved that unless data is explicitly stripped or end-to-end encrypted, it leaves a massive trail of passive intelligence.
3. **Building to Understand:** Writing these tools from scratch—rather than just using Nmap, Wireshark, or Suricata—demystified the underlying protocols (TCP, UDP, ICMP) and how operating systems handle network traffic.

## What's Next?
With a solid understanding of offensive recon and network traffic from Week 1, Week 2 shifts the focus towards the **Blue Team** and system defense, starting with Linux hardening, CIS compliance auditing, and system administration.

***
*#30DaysOfCyber*