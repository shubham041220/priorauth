import os
import requests
from dotenv import load_dotenv

load_dotenv()

filename = "inputpdf/form.pdf"

payload = {
    "apikey": "f827a1766e88957",
    "language": "eng",
    "isTable": True,
    "OCREngine": 2,
}

try:
    with open(filename, "rb") as f:
        r = requests.post(
            "https://api.ocr.space/parse/image",
            files={filename: f},
            data=payload,
            timeout=60,
        )

    print("status_code:", r.status_code)
    print("response:", r.text[:2000])
    r.raise_for_status()

except requests.exceptions.RequestException as e:
    print("request failed:", e)
except Exception as e:
    print("other error:", e)
