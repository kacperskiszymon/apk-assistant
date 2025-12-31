# assistant/personality.py

from assistant.identity import APK_IDENTITY


def build_base_response(user_message: str) -> str:
    """
    Bazowa odpowiedź APK – jeszcze bez AI.
    Używana do testów logiki i stylu.
    """

    response = (
        f"{APK_IDENTITY['default_phrase']} "
        "Proszę powiedzieć, w czym mogę pomóc lub jaki jest powód kontaktu. "
        "Jeżeli chce Pan/Pani, mogę również przekazać tę sprawę dalej — "
        "wystarczy zostawić dane kontaktowe."
    )

    return response
