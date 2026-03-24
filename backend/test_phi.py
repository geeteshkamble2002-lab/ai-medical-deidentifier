from services.ocr_service import extract_text
from services.phi_detector import detect_all_phi

file_path = "temp/CBC-absolute-count-test-report.pdf"

text = extract_text(file_path)
results = detect_all_phi(text)

print("\n--- FINAL PHI DETECTIONS ---\n")

for r in results:
    print(f"{r['entity_type']} → {r['text']}")