from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid

from memory.store import init_db, save_message, save_lead
from assistant.ai import ask_apk_ai
from assistant.identity import APK_IDENTITY
from assistant.rules import should_handover_to_human
from intents.detect import detect_intent
from intents.lead_detect import extract_email, extract_phone

app = Flask(__name__)
CORS(app)

init_db()


@app.route("/", methods=["GET"])
def health_check():
    return jsonify({
        "status": "alive",
        "assistant": APK_IDENTITY["name"],
        "message": APK_IDENTITY["default_phrase"]
    })


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True, silent=True)

    if not data or "message" not in data:
        return jsonify({"error": "Brak lub niepoprawny JSON"}), 400

    user_message = data["message"]
    demo_mode = bool(data.get("demo", False))

    session_id = data.get("session_id") or str(uuid.uuid4())

    # 🔍 WYKRYWANIE KONTAKTU
    email = extract_email(user_message)
    phone = extract_phone(user_message)

    has_contact = False
    if email or phone:
        save_lead(session_id, email=email, phone=phone)
        has_contact = True

    # 🔁 HANDOVER
    if should_handover_to_human(user_message):
        reply = APK_IDENTITY["handover_phrase"]
        save_message(session_id, user_message, reply)

        return jsonify({
            "reply": reply,
            "session_id": session_id,
            "intent": "handover",
            "lead_saved": has_contact
        })

    # 🎯 INTENCJA
    intent = detect_intent(user_message)

    # 🧠 AI
    reply = ask_apk_ai(
        user_message=user_message,
        intent=intent,
        has_contact=has_contact,
        demo_mode=demo_mode
    )

    save_message(session_id, user_message, reply)

    return jsonify({
        "reply": reply,
        "session_id": session_id,
        "intent": intent,
        "lead_saved": has_contact
    })


if __name__ == "__main__":
    app.run(debug=True)
