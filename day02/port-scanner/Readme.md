# Day 02 — Concurrent TCP Port Scanner

## 30 Days. 30 Challenges.

This is Day 02 of the **30 Days of Cyber** community challenge — 30 days, 30 hands-on cybersecurity projects, built from scratch. After exploring cryptography basics in Day 01, today's project shifts to network reconnaissance — the first fundamental step in both offensive operations (footprinting) and defensive auditing.

The goal: research, learn, understand, and build. No copy-pasting tutorials — just real problem-solving.

---

## What I Built

A fast, concurrent TCP Port Scanner written in Go. 

Scanning thousands of ports one by one sequentially is incredibly slow. Instead, this tool leverages Go's native concurrency model to implement a **Worker Pool** architecture, allowing it to scan multiple ports simultaneously without overwhelming the host system or crashing the network.

---

## How It Works

Run the compiled Go program and pass the target IP or hostname as an argument. You can also use flags to customize the number of concurrent workers and the maximum port to scan.

```bash
# Basic usage (default: 10 workers, up to port 1024)
go run main.go scanme.nmap.org

# Advanced usage (e.g., 100 workers, up to port 5000)
go run main.go -w 100 -p 5000 scanme.nmap.org
```

**Output example:**
```text
Scanning scanme.nmap.org up to port 5000 with 100 workers...
[+] Port 22 open
[+] Port 80 open

Found 2 open ports
```

---

## The Architecture Explained

### 1. The Worker Pool Pattern

Spawning a new thread for every single port (e.g., 65,535 threads at once) can lead to socket exhaustion or trigger Intrusion Detection Systems (IDS). To solve this, I used a Worker Pool:
- A fixed number of "workers" (Goroutines) are spawned at the start.
- They constantly pull port numbers from a queue, test them, and grab the next one.
- This keeps concurrency high but perfectly controlled.

### 2. Channels (Data Pipelines)

Go handles communication between concurrent threads using Channels.
- **Jobs Channel (`jobs <-chan int`):** A single Goroutine loops from 1 to the max port and feeds these numbers into the channel. Workers pull from this channel.
- **Results Channel (`results chan<- int`):** When a worker finds an open port, it sends that specific port number into the results channel to be printed by the main program.

### 3. Synchronization (WaitGroups)

Because Goroutines run in the background, the main program might finish and exit before the workers are done. 
- I used `sync.WaitGroup` to track active workers. 
- `wg.Add(1)` registers a worker, and `defer wg.Done()` signals when it finishes.
- `wg.Wait()` pauses the main program's teardown until every port has been checked.

### 4. TCP Dialing & Timeouts

The actual port checking relies on Go's `net` package.

**How it works:**
- It securely concatenates the host and port (`net.JoinHostPort`).
- It attempts a TCP handshake using `net.DialTimeout`.
- A strict 500ms timeout prevents the scanner from hanging indefinitely on silently dropped packets (filtered ports).
- If `err == nil`, the connection succeeded, meaning the port is OPEN. The socket is then cleanly closed to avoid resource leaks.

---

## Project Structure

```text
port-scanner/
├── go.mod            # Go module file (dependency tracking)
├── main.go           # The main Go source code (CLI parsing, Worker Pool, Network logic)
└── README.md         # This file
```

---

## What I Learned

- **Go Concurrency:** Mastering `Goroutines` to run tasks asynchronously.
- **Safe Memory Communication:** Using `Channels` to safely pass data between Goroutines without race conditions.
- **Thread Synchronization:** Using `sync.WaitGroup` to orchestrate background tasks.
- **Network Fundamentals:** Understanding TCP handshakes and handling timeouts to differentiate between closed and filtered ports.
- **CLI Development in Go:** Using the `flag` package to parse command-line arguments and generate automatic help menus.

---

**#30DaysOfCyber**