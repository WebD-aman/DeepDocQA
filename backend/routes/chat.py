from flask import Blueprint, current_app, jsonify, request


chat_bp = Blueprint("chat", __name__)


@chat_bp.post("/ask")
def ask_question():
    payload = request.get_json(silent=True) or {}
    question = (payload.get("question") or "").strip()

    if not question:
        return jsonify({"error": "Question is required."}), 400

    engine = current_app.config["QA_ENGINE"]

    try:
        answer = engine.answer_question(question)
        return jsonify(answer), 200
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception:
        current_app.logger.exception("Question answering failed")
        return jsonify({"error": "Could not answer the question."}), 500
