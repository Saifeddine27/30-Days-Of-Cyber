# Day 01 — Multi-Cipher Encoder/Decoder

## 30 Days. 30 Challenges.

This is Day 01 of the **30 Days of Cyber** community challenge — 30 days, 30 hands-on cybersecurity projects, built from scratch. Each day connects to the ones before it, starting from the basics and climbing toward real offensive/defensive scenarios.

The goal: research, learn, understand, and build. No copy-pasting tutorials — just real problem-solving.

---

## What I Built

A command-line multi-cipher tool that can encode and decode text using four different methods:

- Caesar Cipher
- Base64 Encoding
- Vigenère Cipher
- Hexadecimal Encoding

---

## How It Works

Run `python main.py`, pick a cipher, choose encrypt or decrypt, enter your message, and get the result.

---

## The Ciphers Explained

### 1. Caesar Cipher

A substitution cipher where each letter is shifted by a fixed number of positions in the alphabet.

**How it works:**
- Take each letter, find its position (0–25) using `ord()`.
- Add the shift value.
- Use modulo 26 (`% 26`) to wrap around if it goes past Z.
- Convert back to a letter using `chr()`.

**Formula:** `chr((ord(char) - 97 + shift) % 26 + 97)`

Example: `hello` with shift 5 → `mjqqt`

To decrypt, the algorithm simply subtracts the shift instead of adding it (passing `-shift`).

---

### 2. Base64 (Built from scratch)

An encoding scheme that converts binary data into a set of 64 printable ASCII characters. Instead of using Python's built-in library, this tool implements the algorithm manually using raw bitwise operations.

**How it works:**
- Pad the string with null bytes (`\x00`) if its length isn't a multiple of 3.
- Group 3 characters (3 bytes = 24 bits) into a single integer using bitwise left-shifts (`<<`) and OR operators (`|`).
- Slice that 24-bit block into four 6-bit chunks using right-shifts (`>>`) and a bitmask (`& 63`).
- Map each 6-bit chunk to the Base64 dictionary.
- Replace artificial padded bytes with `=` at the end.

**Base64 alphabet:** `ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/`

Example: `hello` → `aGVsbG8=`

To decode, the process is perfectly reversed using a reverse dictionary and the `& 255` mask to extract the original 8-bit characters.

---

### 3. Vigenère Cipher

A polyalphabetic cipher that uses a keyword to determine different shift values for each letter. This implementation relies on a mathematical matrix approach.

**How it works:**
- Generates a complete 26x26 Tabula Recta (Vigenère square) dynamically using a `NumPy` matrix.
- Extends the keyword string to match the exact length of the message.
- **Encrypt:** Uses the message character as the column index and the key character as the row index to locate the encrypted value in the matrix.
- **Decrypt:** Identifies the key's row, then uses `np.where()` to scan that row for the ciphertext value and retrieve the original column index.

Example: `helloworld` with key `cle` → `jpwPqhzvph`

---

### 4. Hex

The simplest encoding — each character is converted to its 2-digit hexadecimal ASCII value.

**How it works:**
- **Encode:** `ord(char)` gets the ASCII decimal, then `format(val, '02x')` converts it to a guaranteed 2-digit hex string.
- **Decode:** Reads the string in chunks of 2 characters (`pair = ch[i:i+2]`), converts base-16 back to an integer `int(pair, 16)`, and parses it back to text with `chr()`.

Example: `Hi` → `4869`

---

## Project Structure

```text
cipher-tool/
├── main.py           # CLI menu — ties everything together
├── caesar.py         # Caesar cipher encrypt/decrypt functions
├── base64_algo.py    # Base64 encode/decode functions (manual bitwise implementation)
├── vigenere.py       # Vigenère cipher encrypt/decrypt functions (NumPy Matrix)
├── hex_algo.py       # Hex encode/decode functions
└── README.md         # This file
