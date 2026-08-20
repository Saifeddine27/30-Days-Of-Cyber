"""
HASH CRACKER CLI Tool
Main entry point to test .
"""

import hash_cracker
import string
import time

def main():
    print("-" * 30)
    print("      HASH CRACKER TOOL      ")
    print("-" * 30)
    print("1. Dictionary")
    print("2. Brute Force")
    print("3. Dictionary + rules")
    print("4. Dictionary (Multiprocess)")
    
    choice = input("Pick (1, 2, 3 or 4): ").strip()

    if choice == "1":
        target = input("Enter hash to crack: ")
        wordlist = input("Enter wordlist path: ")
        hash_type = hash_cracker.detect_hash(target)
        
        print("\n" + "=" * 30)
        print(f"Cracking Hash: {target}")
        print(f"Detected hash type: {hash_type}")
        print("=" * 30)
        
        result = hash_cracker.dict_cracker(target, hash_type, wordlist)
        
        if result:
            print(f"CRACKED: {result}")
        else:
            print("Not found in wordlist")
        print("=" * 30 + "\n")

    elif choice == "2":
        target = input("Enter hash to crack: ")
        max_length = int(input("Enter max length: "))
        hash_type = hash_cracker.detect_hash(target)
        
        print("\nChoose charset:")
        print("1. Lowercase (a-z)")
        print("2. Lowercase + digits (a-z, 0-9)")
        print("3. Lowercase + uppercase (a-z, A-Z)")
        print("4. All (a-z, A-Z, 0-9, symbols)")
        charset_choice = input("Pick (1-4): ")
        
        if charset_choice == "1":
            charset = string.ascii_lowercase
        elif charset_choice == "2":
            charset = string.ascii_lowercase + string.digits
        elif charset_choice == "3":
            charset = string.ascii_lowercase + string.ascii_uppercase
        elif charset_choice == "4":
            charset = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
        else:
            print("Invalid charset choice. Exiting...")
            return

        print("\n" + "=" * 30)
        print(f"Cracking Hash: {target}")
        print(f"Detected hash type: {hash_type}")
        print("=" * 30)
            
        result = hash_cracker.brute_force_cracker(target, hash_type, max_length, charset)
        
        if result:
            print(f"CRACKED: {result}")
        else:
            print("Not found")
        print("=" * 30 + "\n")

    elif choice == "3":
        target = input("Enter hash to crack: ")
        wordlist = input("Enter wordlist path: ")
        hash_type = hash_cracker.detect_hash(target)
        
        print("\n" + "=" * 30)
        print(f"Cracking Hash: {target}")
        print(f"Detected hash type: {hash_type}")
        print("=" * 30)
        
        result = hash_cracker.crack_rules(target, hash_type, wordlist)
        
        if result:
            print(f"CRACKED: {result}")
        else:
            print("Not found in wordlist or with mutations")
        print("=" * 30 + "\n")

    elif choice == "4":
        target = input("Enter hash to crack: ")
        wordlist = input("Enter wordlist path: ")
        hash_type = hash_cracker.detect_hash(target)
        
        print("\n" + "=" * 30)
        print(f"Cracking Hash: {target}")
        print(f"Detected hash type: {hash_type}")
        print("=" * 30)
        
        start_time = time.time()
        result = hash_cracker.dict_multiprocessing_cracker(target, hash_type, wordlist)
        elapsed = time.time() - start_time
        
        if result:
            print(f"CRACKED: {result} (in {elapsed:.2f}s)")
        else:
            print("Not found in wordlist")
        print("=" * 30 + "\n")

    else:
        print("Invalid choice. Exiting...")
        return

if __name__ == "__main__":
    main()