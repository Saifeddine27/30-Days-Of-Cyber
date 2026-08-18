"""
Multi-Cipher CLI Tool
Main entry point to test Caesar, Vigenere, Base64, and Hex algorithms.
"""

import caesar
import base64_algo
import vigenere
import hex_algo

def main():
    print("-" * 30)
    print("      MULTI-CIPHER TOOL      ")
    print("-" * 30)
    print("1. Caesar Cipher")
    print("2. Base64 Encoding")
    print("3. Vigenere Cipher")
    print("4. Hexadecimal Encoding")
    print("-" * 30)

    choice = input("Pick a cipher (1-4): ")

    if choice not in ["1", "2", "3", "4"]:
        print("Invalid choice. Exiting...")
        return

    mode = input("Choose mode ('e' for encrypt/encode, 'd' for decrypt/decode): ").lower()
    
    if mode not in ["e", "d"]:
        print("Invalid mode. Exiting...")
        return
        
    message = input("Enter your message: ")
    result = ""

    # 1. CAESAR
    if choice == "1":
        try:
            shift = int(input("Enter shift value (integer): "))
        except ValueError:
            print("Error: The shift value must be a number.")
            return
            
        if mode == "e":
            result = caesar.encrypt_text(message, shift)
        else:
            result = caesar.decrypt_text(message, shift)

    # 2. BASE64
    elif choice == "2":
        if mode == "e":
            result = base64_algo.encode_base64(message)
        else:
            result = base64_algo.decode_base64(message)

    # 3. VIGENERE
    elif choice == "3":
        key = input("Enter keyword: ")
        if mode == "e":
            result = vigenere.encrypt_vigenere(message, key)
        else:
            result = vigenere.decrypt_vigenere(message, key)

    # 4. HEXADECIMAL
    elif choice == "4":
        if mode == "e":
            result = hex_algo.encode_hex(message)
        else:
            result = hex_algo.decode_hex(message)

    # Affichage du résultat
    print("\n" + "=" * 30)
    print("RESULT:")
    print(result)
    print("=" * 30 + "\n")


if __name__ == "__main__":
    main()