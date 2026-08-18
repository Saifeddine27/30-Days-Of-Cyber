"""
Hexadecimal Encoder/Decoder
Provides functions to convert plain text to a hexadecimal string and vice versa.
"""

def encode_hex(text: str) -> str:
    """
    Converts a plain text string into its hexadecimal representation.
    Each character is converted to a 2-digit hex value.
    """
    encoded_text = ""
    for char in text:
        hex_char = format(ord(char), '02x')
        encoded_text += hex_char
        
    return encoded_text

def decode_hex(hex_string: str) -> str:
    """
    Converts a continuous hexadecimal string back into plain text.
    Reads the string in pairs of 2 characters.
    """
    decoded_text = ""
    for i in range(0, len(hex_string), 2):
        pair = hex_string[i:i+2]
        decoded_char = chr(int(pair, 16))
        decoded_text += decoded_char
        
    return decoded_text