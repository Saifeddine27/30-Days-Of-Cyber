"""
Caesar Cipher Implementation
Provides functions to encrypt and decrypt text using a Caesar cipher.
"""

def encrypt_char(char: str, shift: int) -> str:
    """
    Encrypts a single character by a given shift.
    Leaves non-alphabetic characters (like spaces and punctuation) unchanged.
    """
    shift = shift % 26
    encrypted_char = char 
    
    if 'a' <= char <= 'z':
        new_index = (ord(char) - ord('a') + shift) % 26
        encrypted_char = chr(ord('a') + new_index)
    elif 'A' <= char <= 'Z':
        new_index = (ord(char) - ord('A') + shift) % 26
        encrypted_char = chr(ord('A') + new_index)
        
    return encrypted_char

def encrypt_text(text: str, shift: int) -> str:
    """
    Encrypts a full string using the Caesar cipher.
    """
    return "".join(encrypt_char(char, shift) for char in text)

def decrypt_text(text: str, shift: int) -> str:
    """
    Decrypts a Caesar cipher string using the original shift.
    """
    # Decrypting is simply shifting backwards by the same amount
    return encrypt_text(text, -shift)