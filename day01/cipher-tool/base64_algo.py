"""
Custom Base64 Encoder/Decoder
Provides functions to encode plain text into Base64 and decode it back,
using pure bitwise operations.
"""

import string

# --- Global Constants ---
ALPHABET_BASE64 = string.ascii_uppercase + string.ascii_lowercase + string.digits + "+/"
ENCODE_DICT = {i: char for i, char in enumerate(ALPHABET_BASE64)}
DECODE_DICT = {char: i for i, char in enumerate(ALPHABET_BASE64)}


def encode_base64(text: str) -> str:
    """
    Encodes a plain text string into Base64 format.
    Uses padding (=) if the text length is not a multiple of 3.
    """
    encoded_text = ""
    remainder = len(text) % 3

    # Pad the string with null bytes (\x00) if it's not a multiple of 3
    if remainder == 2:
        text_padded = text + "\x00"       
    elif remainder == 1:
        text_padded = text + "\x00\x00"
    else:
        text_padded = text
        
    # Process the text in blocks of 3 characters (24 bits)
    for i in range(0, len(text_padded), 3):
        v1 = ord(text_padded[i])
        v2 = ord(text_padded[i+1])
        v3 = ord(text_padded[i+2])
        
        # Combine 3 bytes into a 24-bit integer
        bloc = (v1 << 16) | (v2 << 8) | v3
        
        # Extract four 6-bit chunks
        index1 = (bloc >> 18) & 63
        index2 = (bloc >> 12) & 63
        index3 = (bloc >> 6) & 63
        index4 = bloc & 63
        
        encoded_text += ENCODE_DICT[index1] + ENCODE_DICT[index2] + ENCODE_DICT[index3] + ENCODE_DICT[index4]
        
    # Replace the artificial characters with padding "="
    if remainder == 2:
        return encoded_text[:-1] + "="   
    elif remainder == 1:
        return encoded_text[:-2] + "=="  
        
    return encoded_text


def decode_base64(b64_string: str) -> str:
    """
    Decodes a Base64 string back into plain text.
    Automatically cleans spaces and newlines before decoding.
    """
    # Clean the input (Base64 blocks often contain formatting spaces/newlines)
    b64_string = b64_string.replace(" ", "").replace("\n", "").replace("\r", "")
    
    n = len(b64_string)
    decoded_text = ""
    
    # Process the text in blocks of 4 characters
    for i in range(0, n, 4):
        l1 = b64_string[i]
        l2 = b64_string[i+1]
        l3 = b64_string[i+2]
        l4 = b64_string[i+3]
        
        v1 = DECODE_DICT[l1]
        v2 = DECODE_DICT[l2]
        v3 = DECODE_DICT[l3] if l3 != "=" else 0
        v4 = DECODE_DICT[l4] if l4 != "=" else 0
        
        # Combine the four 6-bit values back into a 24-bit integer
        bloc = (v1 << 18) | (v2 << 12) | (v3 << 6) | v4
        
        # Extract the three original 8-bit bytes
        index1 = (bloc >> 16) & 255
        index2 = (bloc >> 8) & 255
        index3 = bloc & 255
        
        decoded_text += chr(index1)
        if l3 != "=":
            decoded_text += chr(index2)
        if l4 != "=":
            decoded_text += chr(index3)
            
    return decoded_text
