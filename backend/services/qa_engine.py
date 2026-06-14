import os
import shutil
from datetime import datetime, timezone

import numpy as np
from werkzeug.utils import secure_filename

from services.chunker import chunk_text
from services.docx_reader import read_docx
from services.embedding_service import EmbeddingService
from services.pdf_reader import read_pdf
from services.text_processor import clean_text, format_readable_answer


class QAEngine:
    def __init__(self, upload_dir, confidence_threshold=0.35):
        self.upload_dir = upload_dir
        self.confidence_threshold = confidence_threshold
        self.embedding_service = EmbeddingService()
        self.current_document = None
        self.current_path = None
        self.chunks = []
        self.chunk_embeddings = np.empty((0, 256), dtype=np.float32)
        os.makedirs(self.upload_dir, exist_ok=True)

    def replace_document(self, file_storage):
        self.clear_current_document()

        filename = secure_filename(file_storage.filename)
        if not filename:
            raise ValueError("Invalid file name.")

        path = os.path.join(self.upload_dir, filename)
        file_storage.save(path)

        text = self._extract_text(path)
        text = clean_text(text)
        if not text:
            self.clear_current_document()
            raise ValueError("The document does not contain readable text.")

        self.chunks = chunk_text(text)
        if not self.chunks:
            self.clear_current_document()
            raise ValueError("Could not create searchable text chunks from the document.")

        self.chunk_embeddings = self.embedding_service.embed_texts(self.chunks)
        self.current_document = filename
        self.current_path = path

        return {
            "message": "Document uploaded and processed successfully.",
            "current_document": self.current_document,
            "chunk_count": len(self.chunks),
            "using_trained_model": self.embedding_service.using_trained_model,
        }

    def clear_current_document(self):
        self.current_document = None
        self.current_path = None
        self.chunks = []
        self.chunk_embeddings = np.empty((0, 256), dtype=np.float32)

        if os.path.isdir(self.upload_dir):
            for item in os.listdir(self.upload_dir):
                item_path = os.path.join(self.upload_dir, item)
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)

    def answer_question(self, question):
        if not self.current_document or not self.chunks:
            raise ValueError("Please upload a document before asking questions.")

        question_embedding = self.embedding_service.embed_texts([question])[0]
        similarities = self.chunk_embeddings @ question_embedding
        best_index = int(np.argmax(similarities))
        confidence = float(similarities[best_index])
        source_chunk = self.chunks[best_index]

        effective_threshold = self.confidence_threshold if self.embedding_service.using_trained_model else 0.1

        if confidence < effective_threshold:
            answer = "I could not find sufficient information in the current document."
        else:
            answer = format_readable_answer(source_chunk)

        return {
            "answer": answer,
            "confidence": round(confidence, 4),
            "source_chunk": source_chunk,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def _extract_text(self, path):
        extension = os.path.splitext(path)[1].lower()
        if extension == ".pdf":
            return read_pdf(path)
        if extension == ".docx":
            return read_docx(path)
        if extension == ".txt":
            with open(path, "r", encoding="utf-8", errors="ignore") as file:
                return file.read()
        raise ValueError("Unsupported file type.")
