"""
METADATA SCRUBBER CLI Tool
Main entry point.
"""

import os
import metadata_scrubber

def main():
    print("-" * 30)
    print("    METADATA SCRUBBER TOOL    ")
    print("-" * 30)
    print("1. Extract Metadata (Single File)")
    print("2. Scrub Metadata (Single File)")
    print("3. Bulk Scrub Directory (Batch Mode)")
    
    choice = input("Pick (1, 2, or 3): ").strip()
    if choice not in ["1", "2", "3"]:
        print("Invalid choice. Exiting...")
        return

    if choice in ["1", "2"]:
        file_path = input("Enter file path: ").strip()
        
        if not os.path.exists(file_path):
            print(f"Critical Error: File '{file_path}' not found.")
            return

        ext = file_path.lower().split('.')[-1]
        print("\n" + "=" * 30)
        
        if choice == "1":
            print(f"Extracting Metadata from: {file_path}")
            print("=" * 30)
            if ext in ["jpg", "jpeg"]:
                metadata_scrubber.extract_image_metadata(file_path)
            elif ext == "pdf":
                metadata_scrubber.extract_pdf_metadata(file_path)
            elif ext in ["xlsx", "pptx", "docx"]:
                metadata_scrubber.extract_office_metadata(file_path)
            else:
                print(f"Format '.{ext}' not supported for extraction.")
                
        elif choice == "2":
            output_path = input("Enter output path (e.g., clean_photo.jpg): ").strip()
            print(f"Scrubbing Metadata from: {file_path}")
            print("=" * 30)
            if ext in ["jpg", "jpeg"]:
                metadata_scrubber.scrub_image_metadata(file_path, output_path)
            elif ext == "pdf":
                metadata_scrubber.scrub_pdf_metadata(file_path, output_path)
            elif ext in ["xlsx", "pptx", "docx"]:
                metadata_scrubber.scrub_office_metadata(file_path, output_path)
            else:
                print(f"Format '.{ext}' not supported for scrubbing.")
                
        print("=" * 30 + "\n")

    elif choice == "3":
        input_dir = input("Enter source directory path: ").strip()
        output_dir = input("Enter destination directory path: ").strip()
        
        if not os.path.isdir(input_dir):
            print(f"Critical Error: Directory '{input_dir}' not found.")
            return
            
        if os.path.abspath(input_dir) == os.path.abspath(output_dir):
            print("Critical Error: Source and Destination directories must be different.")
            return
            
        print("\n" + "=" * 30)
        metadata_scrubber.batch_scrub_directory(input_dir, output_dir)
        print("=" * 30 + "\n")

if __name__ == "__main__":
    main()