from openai import OpenAI
from assistant.identity import APK_IDENTITY

client = OpenAI()


def ask_apk_ai(
    user_message: str,
    intent: str,
    has_contact: bool,
    demo_mode: bool = False
) -> str:
    """
    Inteligencja APK z DEMO MODE i kontrolą leadów
    """

    if demo_mode:
        contact_instruction = (
            "To tryb demo. "
            "Nie naciskaj na podanie kontaktu. "
            "Jeśli użytkownik testuje działanie lub zadaje pytania o Ciebie, "
            "wyjaśniaj spokojnie jak funkcjonujesz."
        )
    else:
        if has_contact:
            contact_instruction = (
                "Klient podał już dane kontaktowe. "
                "Podziękuj i poinformuj, że ktoś odezwie się wkrótce. "
                "NIE pytaj ponownie o kontakt."
            )
        else:
            contact_instruction = (
                "Jeśli to naturalne w rozmowie, "
                "zaproponuj pozostawienie adresu e-mail lub numeru telefonu."
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
- NIE powtarzaj pytania o kontakt
- jeśli użytkownik odmawia, zaakceptuj to
- w trybie demo możesz mówić meta (jak działasz)

Tryb demo: {demo_mode}
Kontakt już zapisany: {has_contact}

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
        temperature=0.35
    )

    return response.output_text.strip()
