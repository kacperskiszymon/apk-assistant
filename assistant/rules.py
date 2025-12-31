# assistant/rules.py

def should_handover_to_human(message: str) -> bool:
    """
    Sprawdza, czy sprawa wymaga kontaktu z człowiekiem.
    Na razie bardzo prosta logika.
    """

    keywords = [
        "reklamacja",
        "problem",
        "skarga",
        "prawnik",
        "umowa",
        "faktura"
    ]

    message_lower = message.lower()

    return any(keyword in message_lower for keyword in keywords)
