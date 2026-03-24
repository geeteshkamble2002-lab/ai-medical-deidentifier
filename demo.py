import streamlit as st
import tempfile

from backend.services.ocr_service import extract_text
from backend.services.phi_detector import detect_all_phi
from backend.services.redactor import redact_text


st.set_page_config(page_title="Medical De-Identifier", layout="wide")

st.title("🏥 AI Medical De-Identification System")

st.write("Upload a medical document to detect and redact PHI.")

uploaded_file = st.file_uploader(
    "Upload PDF/Image",
    type=["pdf", "png", "jpg", "jpeg"]
)

if uploaded_file:
    st.info("Processing...")

    # Save temp file
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded_file.read())
        file_path = tmp.name

    # Pipeline
    text = extract_text(file_path)
    entities = detect_all_phi(text)
    redacted = redact_text(text, entities)

    # Layout
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original Text")
        st.text_area("", text, height=400)

    with col2:
        st.subheader("Redacted Text")
        st.text_area("", redacted, height=400)

    # Report
    st.subheader("PHI Report")

    report = {}
    for e in entities:
        report[e["entity_type"]] = report.get(e["entity_type"], 0) + 1

    st.json(report)