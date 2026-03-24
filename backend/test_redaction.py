from services.ocr_service import extract_text
from services.phi_detector import detect_all_phi
from services.redactor import redact_text

text = extract_text("temp/CBC-absolute-count-test-report.pdf")
entities = detect_all_phi(text)

redacted = redact_text(text, entities)

print("\n===== REDACTED OUTPUT =====\n")
print(redacted[:1000])