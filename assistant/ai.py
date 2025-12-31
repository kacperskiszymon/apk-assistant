# assistant/ai.py

from openai import OpenAI
from assistant.identity import APK_IDENTITY

client = OpenAI()


def ask_apk_ai(user_message: str, intent: str, has_contact: bool) -> str:
    """
    Inteligencja APK z logiką leadów
    """

    if has_contact:
        contact_instruction = (
            "Klient podał już dane kontaktowe. "
            "Podziękuj i poinformuj, że ktoś odezwie się wkrótce."
        )
    else:
        contact_instruction = (
            "Jeśli to naturalne, poproś o email lub numer telefonu."
        )

    system_prompt = f"""
Jesteś {APK_IDENTITY['name']} ({APK_IDENTITY['short_name']}).

Styl:
- formalny
- spokojny
- rzeczowy
- ludzki

Zasady:
- nie sprzedajesz agresywnie
- nie lej wody
- zawsze dążysz do kontaktu
- jeśli kontakt już jest, nie pytaj ponownie

Aktualna intencja klienta: {intent}

Instrukcja kontaktu:
{contact_instruction}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        temperature=0.4
    )

    return response.output_text.strip()
