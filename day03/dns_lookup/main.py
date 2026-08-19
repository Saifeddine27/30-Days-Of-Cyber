"""
DNS LOOKUP CLI Tool
Main entry point to test .
"""

import dns_lookup
import dns.resolver

def check_domain_exists(domain: str) -> bool:
    try:
        # Si on trouve un SOA ou un NS, le domaine existe.
        dns.resolver.resolve(domain, 'SOA')
        return True
    except dns.resolver.NXDOMAIN:
        return False
    except Exception:
        return True
    
def main():
    print("-" * 30)
    print("      DNS-LOOKUP TOOL      ")
    print("-" * 30)
    print("1. Domain lookup")
    print("2. Reverse lookup (Ip to Hostname)")
    choice = input("Pick (1 or 2): ")

    if choice == "1":
        domain = input("Enter domain: ")
        print("\n" + "=" * 30)
        print(f"DNS Lookup for {domain}")
        print("=" * 30)
        if not check_domain_exists(domain):
            print(f"\nCritical Error: The domain '{domain}' does not exist (NXDOMAIN).")
        else:
            dns_lookup.get_a(domain)
            dns_lookup.get_aaaa(domain)
            dns_lookup.get_mx(domain)
            dns_lookup.get_ns(domain)
            dns_lookup.get_txt(domain)
            dns_lookup.get_cname(domain) 
        print("=" * 30 + "\n")
    elif choice == "2":
        ip = input("Enter IP address: ")
        print("\n" + "=" * 30)
        print(f"Reverse DNS for {ip}")
        dns_lookup.reverse_lookup(ip)
        print("=" * 30 + "\n")
    else:
        print("Invalid choice. Exiting...")
        return

if __name__ == "__main__":
    main()