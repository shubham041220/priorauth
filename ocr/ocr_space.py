# ocr/ocr_space.py
# ── Implementation — defines HOW OCR Space does it ────────────────────

import os
import requests
import fitz
from dotenv import load_dotenv
from ocr.ocrprotocol import OCRProtocol

load_dotenv()

class OCRSpaceClient(OCRProtocol):

    def ocr(self, filename: str) -> str:
        """Entry point — checks pages and chooses function."""

        pdf = fitz.open(filename)
        total_pages = len(pdf)
        pdf.close()

        print(f"Total pages: {total_pages}")

        if total_pages <= 3:
            print("Using simple OCR...")
            return self._ocr_simple(filename)
        else:
            print("Using chunked OCR...")
            return self._ocr_chunked(filename)

    def _ocr_simple(self, filename: str) -> str:
        """For PDFs with 3 or fewer pages."""

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

    def _ocr_chunked(self, filename: str) -> str:
        """For PDFs with more than 3 pages."""

        pdf = fitz.open(filename)
        total_pages = len(pdf)
        full_text = ""

        for start in range(0, total_pages, 3):
            end = min(start + 3, total_pages)
            print(f"Processing pages {start+1} to {end} of {total_pages}...")

            chunk_pdf = fitz.open()
            chunk_pdf.insert_pdf(pdf, from_page=start, to_page=end-1)
            chunk_path = f"temp_chunk_{start}.pdf"
            chunk_pdf.save(chunk_path)
            chunk_pdf.close()

            chunk_text = self._ocr_simple(chunk_path)
            if chunk_text:
                full_text += chunk_text

            os.remove(chunk_path)

        pdf.close()
        return full_text