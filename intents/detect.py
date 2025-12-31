# intents/detect.py

def detect_intent(message: str) -> str:
    """
    Rozpoznaje intencję użytkownika na podstawie słów kluczowych.
    Zwraca jedną z wartości:
    - offer
    - price
    - booking
    - contact
    - other
    """

    msg = message.lower()

    if any(word in msg for word in ["oferta", "usługa", "co robicie", "zakres"]):
        return "offer"

    if any(word in msg for word in ["cena", "koszt", "ile", "płatność"]):
        return "price"

    if any(word in msg for word in ["termin", "rezerwacja", "zapisać", "spotkanie"]):
        return "booking"

    if any(word in msg for word in ["kontakt", "email", "telefon", "numer"]):
        return "contact"

    return "other"
