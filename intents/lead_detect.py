# intents/lead_detect.py

import re


def extract_email(message: str):
    match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", message)
    return match.group(0) if match else None


def extract_phone(message: str):
    match = re.search(r"(\+?\d[\d\s\-]{7,}\d)", message)
    return match.group(0) if match else None
