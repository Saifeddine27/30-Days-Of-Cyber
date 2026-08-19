import dns.resolver
import dns.reversename


resolver = dns.resolver.Resolver()
resolver.nameservers = ['8.8.8.8', '8.8.4.4']

def _fetch_record(domain: str, record_type: str) -> None:
    try:
        answers = resolver.resolve(domain, record_type)
        
        for answer in answers:
            print(f" {record_type} Record: {answer}")

    except dns.resolver.NoAnswer:
        print(f" Info: No '{record_type}' record found for '{domain}'.")
    except dns.resolver.Timeout:
        print(f" Error: The DNS server timed out for '{record_type}' query.")
    except dns.resolver.NoNameservers:
        print(f" Error: No DNS servers could answer the '{record_type}' query.")
    except Exception as e:
        print(f" An unknown error occurred ({record_type}): {e}")

def get_a(domain: str) -> None:
    _fetch_record(domain, 'A')

def get_aaaa(domain: str) -> None:
    _fetch_record(domain, 'AAAA')

def get_mx(domain: str) -> None:
    _fetch_record(domain, 'MX')

def get_ns(domain: str) -> None:
    _fetch_record(domain, 'NS')

def get_txt(domain: str) -> None:
    _fetch_record(domain, 'TXT')

def get_cname(domain: str) -> None:
    _fetch_record(domain, 'CNAME')

def reverse_lookup(ip: str) -> None:
    try:
        rev_name = dns.reversename.from_address(ip)
        _fetch_record(rev_name, 'PTR')
    except Exception as e:
        print(f" Reverse DNS: Error - {e}")