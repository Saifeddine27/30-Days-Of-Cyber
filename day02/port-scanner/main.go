package main

import (
	"flag"
	"fmt"
	"net"
	"sync"
	"time"
)

func isOpen(network, host string, port int) bool {
	address := net.JoinHostPort(host, fmt.Sprintf("%d", port))

	conn, err := net.DialTimeout(network, address, 500*time.Millisecond)
	if err != nil {
		return false
	}
	conn.Close()
	return true
}

func worker(network, host string, jobs <-chan int, results chan<- int, wg *sync.WaitGroup) {
	defer wg.Done()

	for port := range jobs {
		if isOpen(network, host, port) {
			results <- port
		}
	}
}

func main() {

	numWorkers := flag.Int("w", 10, "Nombre de workers simultanés")
	maxPort := flag.Int("p", 1024, "Port maximum à scanner")

	flag.Parse()

	if flag.NArg() != 1 {
		fmt.Println("Usage: go run main.go [options] <host>")
		fmt.Println("Exemple: go run main.go -w 100 -p 5000 scanme.nmap.org")
		flag.PrintDefaults()
		return
	}

	host := flag.Arg(0)
	network := "tcp"

	fmt.Printf("Scanning %s up to port %d with %d workers...\n", host, *maxPort, *numWorkers)

	jobs := make(chan int)
	results := make(chan int)

	var wg sync.WaitGroup

	// 1. Launch workers
	for i := 0; i < *numWorkers; i++ {
		wg.Add(1)
		go worker(network, host, jobs, results, &wg)
	}

	// 2. Send jobs
	go func() {
		for port := 1; port <= *maxPort; port++ {
			jobs <- port
		}
		close(jobs)
	}()

	// 3. Close results when workers finish
	go func() {
		wg.Wait()
		close(results)
	}()

	// 4. Read results
	count := 0
	for port := range results {
		fmt.Printf("[+] Port %d open\n", port)
		count++
	}

	fmt.Printf("\nFound %d open ports\n", count)
}
