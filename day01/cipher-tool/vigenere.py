"""
Vigenere Cipher Implementation
Provides functions to encrypt and decrypt text using a Vigenere cipher 
and a NumPy-generated 26x26 Tabula Recta (Vigenere square).
"""

import numpy as np

# --- Global Constants ---
# Create a 26x26 matrix of integers for the Vigenere square
VIGENERE_MATRIX = np.zeros((26, 26), dtype=int)
for i in range(26):
    for j in range(26):
        VIGENERE_MATRIX[i, j] = (i + j) % 26


def encrypt_vigenere(text: str, key: str) -> str:
    """
    Encrypts a plain text string using the Vigenere cipher.
    Preserves the case of the original text and ignores punctuation.
    """
    key = key.lower()
    n = len(text)
    
    # Extend the key to match the length of the text
    extended_key = (key * (n // len(key) + 1))[:n]
    
    encrypted_text = ""
    for i in range(n):
        char = text[i]
        
        if 'a' <= char <= 'z':
            col = ord(char) - ord('a')
            row = ord(extended_key[i]) - ord('a')
            code = VIGENERE_MATRIX[row, col] + ord('a')
            encrypted_text += chr(code)
            
        elif 'A' <= char <= 'Z':
            col = ord(char) - ord('A')
            row = ord(extended_key[i]) - ord('a') 
            code = VIGENERE_MATRIX[row, col] + ord('A')
            encrypted_text += chr(code)
            
        else:
            encrypted_text += char

    return encrypted_text


def decrypt_vigenere(text: str, key: str) -> str:
    """
    Decrypts a Vigenere cipher string back to plain text.
    Uses NumPy's `where` function to locate the original column.
    """
    key = key.lower()
    n = len(text)
    extended_key = (key * (n // len(key) + 1))[:n]
    
    decoded_text = ""
    for i in range(n):
        char = text[i]
        
        if 'a' <= char <= 'z':
            row = ord(extended_key[i]) - ord('a')
            cipher_val = ord(char) - ord('a')
            
            # Find the column index where the cipher value is located in the row
            col = np.where(VIGENERE_MATRIX[row] == cipher_val)[0][0]
            decoded_text += chr(col + ord('a'))
            
        elif 'A' <= char <= 'Z':
            # Bug fix: The key is always lowercase, so we subtract ord('a') for the row
            row = ord(extended_key[i]) - ord('a')
            cipher_val = ord(char) - ord('A')
            
            col = np.where(VIGENERE_MATRIX[row] == cipher_val)[0][0]
            decoded_text += chr(col + ord('A'))
            
        else:
            decoded_text += char

    return decoded_text
