"""
OCR Service

✔ PDF text extraction
✔ OCR fallback for scanned docs
"""

import pytesseract
from pdf2image import convert_from_path
import pdfplumber


def extract_text(file_path: str) -> str:
    # Try direct PDF extraction first
    try:
        text = ""

        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""

        # If text is too small → fallback to OCR
        if len(text.strip()) < 50:
            return ocr_pdf(file_path)

        return text

    except:
        return ocr_pdf(file_path)


def ocr_pdf(file_path: str) -> str:
    images = convert_from_path(file_path)

    text = ""

    for img in images:
        text += pytesseract.image_to_string(img)

    return text