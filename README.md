# 🏥 AI-Powered HIPAA Medical De-Identification System

## 📌 Overview

Healthcare systems generate vast amounts of unstructured medical data such as lab reports, discharge summaries, and clinical notes. These documents often contain **Protected Health Information (PHI)**, which must be removed to comply with **HIPAA regulations** before using the data for research or AI model training.

This project implements an **end-to-end automated de-identification system** that:

* Detects PHI in medical documents
* Redacts sensitive information
* Preserves clinical meaning
* Provides a structured audit report

---

## 🚀 Key Features

* 📄 **Multi-format Support**
  Handles PDFs, scanned documents, and images

* 🔍 **Hybrid PHI Detection Engine**
  Combines rule-based (regex) + NLP (Presidio)

* 🔒 **Accurate Redaction Engine**
  Replaces PHI with meaningful placeholders

* 🧠 **Context Preservation**
  Ensures medical information remains usable

* 📊 **Redaction Report**
  Summarizes detected PHI types

* 🌐 **Interactive Web UI**
  Upload documents and view before/after comparison

* 🐳 **Dockerized Deployment**
  Fully containerized system using Docker Compose

---

## 🏗️ System Architecture

```
User Upload → OCR → PHI Detection → Redaction → Output + Report
```

### 🔧 Components

#### 1. OCR Layer

* `pdfplumber` → Extracts text from digital PDFs
* `pytesseract` → OCR fallback for scanned documents

#### 2. PHI Detection Engine

* **Regex-based detection**:

  * Phone numbers
  * Emails
  * URLs
  * IDs
  * Structured names (e.g., "Yash M. Patel")

* **NLP-based detection (Presidio)**:

  * Locations
  * Dates & time

#### 3. Redaction Engine

* Span-based replacement (safe & non-overlapping)
* Uses placeholders instead of deletion

#### 4. Backend API

* Built with FastAPI
* Handles file uploads and processing pipeline

#### 5. Frontend

* Simple HTML + JavaScript interface
* Displays:

  * Original text
  * Redacted text
  * PHI report

---

## 🧠 Design Decisions

### 🔹 Hybrid Detection Strategy

Instead of relying solely on ML models, a **hybrid approach** was used:

| Method         | Strength                      |
| -------------- | ----------------------------- |
| Regex          | High precision, deterministic |
| NLP (Presidio) | Context awareness             |

This improves:

* Accuracy
* Explainability
* Stability

---

### 🔹 Context Preservation

Instead of removing text:

```
Hiren Shah → [PATIENT_NAME]
```

This ensures:

* Medical meaning is retained
* Data remains useful for downstream tasks

---

### 🔹 OCR Strategy

1. Attempt direct text extraction
2. If text is insufficient → fallback to OCR
3. Combine outputs for robustness

---

## 📦 Project Structure

```
ai-medical-deidentifier/
│
├── backend/
│   ├── services/
│   │   ├── ocr_service.py
│   │   ├── phi_detector.py
│   │   └── redactor.py
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   └── index.html
│
├── docker-compose.yml
└── README.md
```

---

## ⚙️ Installation & Setup

---

### 🔹 Option 1: Run with Docker (Recommended)

```bash
docker-compose up --build
```

Access:

* Backend API → http://localhost:8000/docs
* Frontend UI → http://localhost:5500

---

### 🔹 Option 2: Run Locally

#### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

#### Frontend

```bash
cd frontend
python -m http.server 5500
```

Open:
👉 http://localhost:5500

---

## 🌐 Usage

1. Upload a medical document (PDF/Image)
2. System processes:

   * OCR extraction
   * PHI detection
   * Redaction
3. View:

   * Original text
   * Redacted text
   * PHI report

---

## 📊 Example Output

### Input:

```
Patient: Hiren Shah  
Phone: 0912345678
```

### Output:

```
Patient: [PATIENT_NAME]  
Phone: [PHONE]
```

### Report:

```json
{
  "PERSON": 3,
  "PHONE_NUMBER": 1,
  "EMAIL_ADDRESS": 1
}
```

---

## 🔐 Compliance Considerations

* Removes key HIPAA identifiers:

  * Names
  * Phone numbers
  * Emails
  * IDs
  * Locations
* Uses placeholders instead of deletion
* Prevents re-identification risks

---

## ⚡ Limitations

* Name detection is rule-based (not fully ML-driven)
* OCR accuracy depends on image quality
* Some over-redaction may occur in noisy text

---

## 🚀 Future Improvements

* Fine-tuned NER model for medical domain
* Handwritten OCR support
* Batch processing dashboard
* Synthetic data generation instead of placeholders

---

## 👨‍💻 Author

**Geetesh Kamble**

---

## ✅ Summary

This project demonstrates:

* End-to-end AI system design
* Practical NLP + OCR integration
* Real-world engineering tradeoffs
* Production-style backend + UI + Docker

👉 Built as part of an AI/ML Software Engineer assignment.
