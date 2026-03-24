"""
FastAPI Backend (Final Production Version)

✔ Clean API
✔ File upload handling
✔ Integrated pipeline
✔ Error-safe
"""

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

import os
import shutil
from collections import Counter

from backend.services.ocr_service import extract_text
from backend.services.phi_detector import detect_all_phi
from backend.services.redactor import redact_text


# -----------------------------
# App Init
# -----------------------------
app = FastAPI(title="AI Medical De-Identifier")

# Enable CORS (for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Temp directory
UPLOAD_DIR = "temp"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# -----------------------------
# Health Check
# -----------------------------
@app.get("/")
def root():
    return {"status": "API running"}


# -----------------------------
# Upload Endpoint
# -----------------------------
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Validate file
        if not file.filename:
            return {"error": "Invalid file"}

        if not file.filename.lower().endswith((".pdf", ".png", ".jpg", ".jpeg", ".txt")):
            return {"error": "Unsupported file type"}

        # Save file
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # -----------------------------
        # Pipeline
        # -----------------------------
        text = extract_text(file_path)

        entities = detect_all_phi(text)

        redacted_text = redact_text(text, entities)

        report = generate_report(entities)

        # Clean up
        try:
            os.remove(file_path)
        except:
            pass

        return {
            "original_text": text,
            "redacted_text": redacted_text,
            "report": report,
            "total_entities": len(entities)
        }

    except Exception as e:
        return {"error": str(e)}


# -----------------------------
# Report Generator
# -----------------------------
def generate_report(entities):
    counter = Counter()

    for e in entities:
        counter[e["entity_type"]] += 1

    return dict(counter)