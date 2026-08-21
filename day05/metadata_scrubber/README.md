# Day 05 — Metadata Scrubber Tool (Anti-OSINT)

**30 Days. 30 Challenges.**

This is Day 05 of the **30 Days of Cyber** community challenge. After exploring offensive techniques like Port Scanning (Day 02) and DNS Enumeration (Day 03), today's project flips the perspective to **Defense and OPSEC (Operational Security)**.

The goal: research, learn, understand, and build a tool that prevents unintentional information leakage through file metadata.

## What I Built

A robust, enterprise-grade **Metadata Scrubber CLI Tool** written in Python. 

Every time a photo is taken or a document is saved, invisible data is embedded into the file (GPS coordinates, software versions, author names). This tool extracts, displays, and securely destroys hidden metadata across multiple file formats (Images, PDFs, and MS Office documents) to protect user privacy. It also features a Bulk Processing engine to scrub entire directory trees automatically.

## How It Works

Run the main Python script to launch the interactive menu.

    # Install dependencies
    pip install -r requirements.txt

    # Run the tool
    python main.py

### Output Example:

    ------------------------------
        METADATA SCRUBBER TOOL    
    ------------------------------
    1. Extract Metadata (Single File)
    2. Scrub Metadata (Single File)
    3. Bulk Scrub Directory (Batch Mode)
    Pick (1, 2, or 3): 1
    Enter file path: evidence.jpg

    ==============================
    Extracting Metadata from: evidence.jpg
    ==============================

    --- 0th Data ---
    Make: Apple
    Model: iPhone 14 Pro
    Software: Adobe Photoshop 2024

    --- GPS Data ---
    GPSLatitude: ((48, 1), (52, 1), (13, 100))
    GPSLongitude: ((2, 1), (19, 1), (59, 100))
    ==============================

## The Architecture & Design Choices

### 1. The "Scalpel vs. Photocopier" Approach (piexif vs Pillow)
To scrub images, I explicitly avoided standard image processing libraries like Pillow. Resaving a JPEG with Pillow causes pixel re-compression, degrading the original image quality. Instead, I used piexif which acts as a hex-editor scalpel: it surgically locates the EXIF byte block, deletes it, and stitches the file back together. **Zero quality loss, zero pixel alteration.**

### 2. Defeating AES-Encrypted PDFs (PyCryptodome)
Many official or administrative PDFs use AES encryption to prevent modification. Standard PDF parsers crash when encountering them. I integrated PyCryptodome alongside PyPDF2 to automatically detect encryption, attempt a default decryption bypass, and cleanly strip the metadata without destroying the document's structure.

### 3. Office Documents as Archives (openpyxl, python-pptx, python-docx)
Modern MS Office files (.docx, .xlsx, .pptx) are actually ZIP archives disguising a structure of XML files. The tool uses specific libraries to unpack these archives in memory, locate the docProps/core.xml file, redact sensitive fields (like Creator and LastModifiedBy), and repack them securely.

### 4. Bulk Processing Engine with OPSEC Fail-Safes
The batch mode uses Python's native os.walk() to recursively clone an entire directory tree. 
**Security feature:** If an unsupported file type is encountered, it is *ignored* and dropped, not copied to the destination. Copying an unscannable file to a "Cleaned" folder gives the user a false sense of security. In OPSEC, fail-safe means dropping the unknown data.

## Project Structure

    metadata_scrubber/
    ├── requirements.txt          # Dependencies (piexif, PyPDF2, pycryptodome, openpyxl, etc.)
    ├── main.py                   # Entry point (CLI Interface & Routing)
    ├── metadata_scrubber.py      # Core logic (Extraction, Scrubbing, Batch Engine)
    └── README.md                 # This file

## What I Learned

* **Data Types in Python:** Handling raw binary bytes extraction from EXIF data and dynamically decoding it to UTF-8 strings.
* **Under-the-hood File Structures:** Discovering that .docx and .xlsx files are just renamed ZIP archives containing XML.
* **Dependency Management:** Understanding how indirect dependencies work (e.g., PyPDF2 requiring PyCryptodome under the hood for AES algorithms).
* **OPSEC Fundamentals:** Seeing firsthand how easily GPS coordinates and internal network usernames can leak through a simple file upload.

***
*#30DaysOfCyber*