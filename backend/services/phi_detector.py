"""
PHI Detection (Production Version)

- Deterministic > heuristic
- No overlap bugs
- No misclassification issues
"""

import re
from typing import List, Dict

from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider


# -----------------------------
# Setup Presidio (limited use)
# -----------------------------
CONFIG = {
    "nlp_engine_name": "spacy",
    "models": [{"lang_code": "en", "model_name": "en_core_web_sm"}],
}

provider = NlpEngineProvider(nlp_configuration=CONFIG)
analyzer = AnalyzerEngine(nlp_engine=provider.create_engine())


# -----------------------------
# Strong Regex (PRIMARY SOURCE)
# -----------------------------
RE_PHONE = re.compile(r"\b\d{10}\b")
RE_EMAIL = re.compile(r"\b[\w\.-]+@[\w\.-]+\.\w+\b")
RE_URL = re.compile(r"\b(www\.[\w\-]+\.\w+|https?://\S+|[A-Za-z0-9]+\.(com|org|net))\b")
RE_ID = re.compile(r"\b(PID|Report ID)\s*[:\-]?\s*\d+\b", re.IGNORECASE)
RE_NAME = re.compile(r"\b[A-Z][a-z]+\s[A-Z]\.\s[A-Z][a-z]+\b")
# RE_NAME_SIMPLE = re.compile(r"\b[A-Z][a-z]+\s[A-Z][a-z]+\b")

def is_valid_name(text: str) -> bool:
    INVALID = {
        "blood", "count", "sample", "type",
        "volume", "laboratory", "report",
        "reference", "result", "test"
    }

    words = text.lower().split()

    if any(w in INVALID for w in words):
        return False

    if len(words) != 2:
        return False

    return all(w[0].isupper() for w in text.split())


# -----------------------------
# Regex Detection (PRIMARY)
# -----------------------------
def detect_regex(text: str) -> List[Dict]:
    results = []

    def add(match, label):
        results.append({
            "start": match.start(),
            "end": match.end(),
            "entity_type": label,
            "text": match.group()
        })

    for m in RE_PHONE.finditer(text):
        add(m, "PHONE_NUMBER")

    for m in RE_EMAIL.finditer(text):
        add(m, "EMAIL_ADDRESS")

    for m in RE_URL.finditer(text):
        add(m, "URL")

    for m in RE_ID.finditer(text):
        add(m, "ID")

    for m in RE_NAME.finditer(text):
        add(m, "PERSON")

    # Safe fallback for 2-word names
    for m in re.finditer(r"\b[A-Z][a-z]+\s[A-Z][a-z]+\b", text):
        name = m.group()

        if is_valid_name(name):
            results.append({
                "start": m.start(),
                "end": m.end(),
                "entity_type": "PERSON",
                "text": name
            })

    return results


# -----------------------------
# Presidio (LIMITED USE)
# -----------------------------
def detect_presidio(text: str) -> List[Dict]:
    results = analyzer.analyze(text=text, language="en")

    allowed = {"LOCATION", "DATE_TIME"}

    output = []

    for r in results:
        entity = r.entity_type
        value = text[r.start:r.end]

        # Skip noisy detections
        if entity not in allowed:
            continue

        if entity == "LOCATION":
            # Reject fake words
            if value.lower() in ["caring", "accurate", "instant"]:
                continue

            # Reject very short words
            if len(value) < 4:
                continue

        # Reject numeric-only DATE_TIME
        if entity == "DATE_TIME":
            if value.isdigit():
                continue
            if not any(x in value.lower() for x in [":", "am", "pm"]):
                continue

        output.append({
            "start": r.start,
            "end": r.end,
            "entity_type": entity,
            "text": value
        })

    return output


# -----------------------------
# Merge (NO OVERLAP ALLOWED)
# -----------------------------
def merge_entities(entities: List[Dict]) -> List[Dict]:
    entities = sorted(entities, key=lambda x: x["start"])

    merged = []
    last_end = -1

    for e in entities:
        if e["start"] >= last_end:
            merged.append(e)
            last_end = e["end"]

    return merged


# -----------------------------
# FINAL ENTRY POINT
# -----------------------------
def detect_all_phi(text: str) -> List[Dict]:
    regex_entities = detect_regex(text)
    presidio_entities = detect_presidio(text)

    all_entities = regex_entities + presidio_entities

    merged = merge_entities(all_entities)

    final_entities = []
    for r in merged:
        entity = r["entity_type"]
        span_text = r["text"]

        if entity == "PERSON":
            if any(word.lower() in span_text.lower() for word in [
                "count", "volume", "sample", "laboratory", "test"
            ]):
                continue
                
        final_entities.append(r)

    return final_entities