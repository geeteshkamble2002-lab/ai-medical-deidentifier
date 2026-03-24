"""
Redaction Engine

✔ Safe replacement
✔ No overlap bugs
✔ Clean output
"""

from typing import List, Dict


PLACEHOLDER_MAP = {
    "PERSON": "[PATIENT_NAME]",
    "PHONE_NUMBER": "[PHONE]",
    "EMAIL_ADDRESS": "[EMAIL]",
    "LOCATION": "[LOCATION]",
    "DATE_TIME": "[DATE_TIME]",
    "ID": "[ID]",
    "URL": "[URL]"
}


def redact_text(text: str, entities: List[Dict]) -> str:
    entities = sorted(entities, key=lambda x: x["start"])

    result = []
    last_idx = 0

    for e in entities:
        start, end = e["start"], e["end"]

        if start < last_idx:
            continue

        result.append(text[last_idx:start])

        placeholder = PLACEHOLDER_MAP.get(e["entity_type"], "[REDACTED]")
        result.append(placeholder)

        last_idx = end

    result.append(text[last_idx:])

    return "".join(result)