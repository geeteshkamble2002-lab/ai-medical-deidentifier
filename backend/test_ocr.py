from services.ocr_service import extract_text

file_path = "temp/CBC-absolute-count-test-report.pdf"

text = extract_text(file_path)

print("\n===== EXTRACTED TEXT =====\n")
print(text[:1000])  # print first 1000 chars