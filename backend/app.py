import os

from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS

from routes.chat import chat_bp
from routes.upload import upload_bp
from services.qa_engine import QAEngine


def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = int(os.getenv("MAX_UPLOAD_MB", "10")) * 1024 * 1024
    app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(__file__), "uploads")
    app.config["QA_ENGINE"] = QAEngine(upload_dir=app.config["UPLOAD_FOLDER"])

    allowed_origins = os.getenv(
        "FRONTEND_ORIGIN",
        "http://localhost:5173,http://127.0.0.1:5173,http://192.168.1.2:5173",
    ).split(",")
    CORS(app, resources={r"/*": {"origins": [origin.strip() for origin in allowed_origins]}})

    app.register_blueprint(upload_bp)
    app.register_blueprint(chat_bp)

    @app.get("/status")
    def status():
        engine = app.config["QA_ENGINE"]
        return jsonify({"current_document": engine.current_document})

    @app.get("/")
    def health():
        return jsonify({"message": "Deep Learning Document QA backend is running"})

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=os.getenv("FLASK_DEBUG") == "1")
