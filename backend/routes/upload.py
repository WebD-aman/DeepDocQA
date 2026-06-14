from flask import Blueprint, current_app, jsonify, request


upload_bp = Blueprint("upload", __name__)

ALLOWED_EXTENSIONS = {"pdf", "txt", "docx"}


def is_allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@upload_bp.post("/upload")
def upload_document():
    if "file" not in request.files:
        return jsonify({"error": "No file was provided."}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Please choose a file to upload."}), 400

    if not is_allowed_file(file.filename):
        return jsonify({"error": "Only PDF, TXT, and DOCX files are supported."}), 400

    engine = current_app.config["QA_ENGINE"]

    try:
        result = engine.replace_document(file)
        return jsonify(result), 200
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception as exc:
        current_app.logger.exception("Document upload failed")
        return jsonify({"error": f"Could not process the document: {exc}"}), 500
