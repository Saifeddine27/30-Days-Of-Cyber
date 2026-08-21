import piexif
from PyPDF2 import PdfReader, PdfWriter
import openpyxl
import docx
from pptx import Presentation
import os

def extract_image_metadata(file_path: str):
    try:
        exif_dict = piexif.load(file_path)
        has_data = False
        for ifd in ("0th", "Exif", "GPS"):
            if exif_dict[ifd]:
                has_data = True
                print(f"\n--- {ifd} Data ---")
                for tag_id in exif_dict[ifd]:
                    tag_name = piexif.TAGS[ifd].get(tag_id, {}).get("name", f"Unknown Tag ({tag_id})")
                    value = exif_dict[ifd][tag_id]
                    if isinstance(value, bytes):
                        try:
                            value = value.decode('utf-8', 'ignore')
                        except:
                            value = "<Binary Data>"
                    print(f"{tag_name}: {value}")
        if not has_data:
            print("No EXIF metadata found in this image.")
    except piexif.InvalidImageDataError:
        print("Error: Invalid JPEG file or format not supported.")
    except Exception as e:
        print(f"Error reading image: {e}")

def scrub_image_metadata(file_path: str, output_path: str):
    try:
        piexif.remove(file_path, output_path)
        print(f"Success! Scrubbed image saved to: {output_path}")
    except Exception as e:
        print(f"Error scrubbing image: {e}")


def extract_pdf_metadata(file_path: str):
    reader = PdfReader(file_path)
    meta = reader.metadata
    try:
        if meta:
            for key,value in meta.items():
                clean_key = key.replace("/","")
                print(f"{clean_key}: {value}")
        else:
            print("No metadata found in this PDF.")
    except Exception as e:
        print(f"Error reading PDF: {e}")



def scrub_pdf_metadata(file_path: str, output_path: str):
    try:
        reader = PdfReader(file_path)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)
        
        writer.add_metadata({})

        with open(output_path, "wb") as f:
            writer.write(f)
        print(f"Success! Scrubbed PDF saved to: {output_path}")
    except Exception as e:
        print(f"Error scrubbing PDF: {e}")

def extract_office_metadata(file_path: str):
    ext = file_path.lower().split('.')[-1]
    try:
        if ext == "xlsx":
            wb = openpyxl.load_workbook(file_path)
            props = wb.properties
        elif ext == "pptx":
            prs = Presentation(file_path)
            props = prs.core_properties
        elif ext == "docx":
            doc = docx.Document(file_path)
            props = doc.core_properties
        else:
            print("Unsupported Office format.")
            return

        print(f"Creator: {props.creator}")
        print(f"Last Modified By: {props.last_modified_by}")
        print(f"Created: {props.created}")
        print(f"Modified: {props.modified}")
        print(f"Title: {props.title}")
    except Exception as e:
        print(f"Error reading Office file: {e}")

def scrub_office_metadata(file_path: str, output_path: str):
    ext = file_path.lower().split('.')[-1]
    try:
        if ext == "xlsx":
            wb = openpyxl.load_workbook(file_path)
            wb.properties.creator = "Redacted"
            wb.properties.last_modified_by = "Redacted"
            wb.properties.title = ""
            wb.save(output_path)
        elif ext == "pptx":
            prs = Presentation(file_path)
            prs.core_properties.creator = "Redacted"
            prs.core_properties.last_modified_by = "Redacted"
            prs.core_properties.title = ""
            prs.save(output_path)
        elif ext == "docx":
            doc = docx.Document(file_path)
            doc.core_properties.creator = "Redacted"
            doc.core_properties.last_modified_by = "Redacted"
            doc.core_properties.title = ""
            doc.save(output_path)
            
        print(f"Success! Scrubbed Office file saved to: {output_path}")
    except Exception as e:
        print(f"Error scrubbing Office file: {e}")


def batch_scrub_directory(input_dir: str, output_dir: str):
    supported_exts = ["jpg", "jpeg", "pdf", "xlsx", "pptx", "docx"]
    scrubbed_count = 0
    skipped_count = 0

    print(f"\nStarting batch process...")
    print(f"Source: {input_dir}")
    print(f"Destination: {output_dir}\n")

    for root, _, files in os.walk(input_dir):
        

        rel_path = os.path.relpath(root, input_dir)
        target_dir = os.path.join(output_dir, rel_path)

        os.makedirs(target_dir, exist_ok=True)

        for file in files:
            ext = file.lower().split('.')[-1]
            input_file_path = os.path.join(root, file)
            output_file_path = os.path.join(target_dir, file)

            if ext in supported_exts:
                print(f"[PROCESS] Scrubbing: {input_file_path}")
                if ext in ["jpg", "jpeg"]:
                    scrub_image_metadata(input_file_path, output_file_path)
                elif ext == "pdf":
                    scrub_pdf_metadata(input_file_path, output_file_path)
                elif ext in ["xlsx", "pptx", "docx"]:
                    scrub_office_metadata(input_file_path, output_file_path)
                scrubbed_count += 1
            else:
                print(f"[SKIP] Unsupported format: {input_file_path}")
                skipped_count += 1

    print("\n" + "=" * 30)
    print("BATCH PROCESSING COMPLETE")
    print(f"Files scrubbed securely: {scrubbed_count}")
    print(f"Files skipped: {skipped_count}")
    print("=" * 30 + "\n")