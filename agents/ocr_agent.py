import os
import requests
from dotenv import load_dotenv
import fitz  # pip install pymupdf

load_dotenv()

def ocr_space_file(filename):
    """Check pages first, then choose which function to run."""

    pdf = fitz.open(filename)
    total_pages = len(pdf)
    pdf.close()

    print(f"Total pages: {total_pages}")

    # ── Choose function based on page count ────────────────────────────
    if total_pages <= 3:
        print("Using existing OCR function...")
        return _ocr_simple(filename)          # your existing function
    else:
        print("Using chunked OCR function...")
        return _ocr_chunked(filename)         # new function for 3+ pages


def _ocr_simple(filename):
    """Your existing function — for PDFs with 3 or fewer pages."""

    payload = {
        "apikey": os.getenv("OCR_API_KEY"),
        "language": "eng",
        "isTable": True,
        "OCREngine": 2,
    }

    with open(filename, "rb") as f:
        r = requests.post(
            "https://api.ocr.space/parse/image",
            files={filename: f},
            data=payload,
        )

    result = r.json()

    if result.get("IsErroredOnProcessing"):
        print("Error:", result.get("ErrorMessage"))
        return None

    full_text = ""
    for page in result.get("ParsedResults", []):
        full_text += page.get("ParsedText", "") + "\n"

    return full_text


def _ocr_chunked(filename):
    """New function — for PDFs with more than 3 pages."""

    pdf = fitz.open(filename)
    total_pages = len(pdf)
    full_text = ""

    for start in range(0, total_pages, 3):
        end = min(start + 3, total_pages)
        print(f"Processing pages {start+1} to {end} of {total_pages}...")

        # Save chunk as temp PDF
        chunk_pdf = fitz.open()
        chunk_pdf.insert_pdf(pdf, from_page=start, to_page=end-1)
        chunk_path = f"temp_chunk_{start}.pdf"
        chunk_pdf.save(chunk_path)
        chunk_pdf.close()

        # OCR the chunk using simple function
        chunk_text = _ocr_simple(chunk_path)
        if chunk_text:
            full_text += chunk_text

        # Delete temp file
        os.remove(chunk_path)

    pdf.close()
    return full_text