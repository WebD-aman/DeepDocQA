import hashlib
import os
import pickle
import re

import numpy as np
from sklearn.preprocessing import normalize


class EmbeddingService:
    def __init__(self, model_dir=None, max_length=80, fallback_dim=256):
        base_dir = os.path.dirname(os.path.dirname(__file__))
        self.model_dir = model_dir or os.path.join(base_dir, "models", "saved_model")
        self.max_length = max_length
        self.fallback_dim = fallback_dim
        self.encoder = None
        self.tokenizer = None
        self.load_error = None
        self.load()

    def load(self):
        encoder_path = os.path.join(self.model_dir, "encoder.keras")
        tokenizer_path = os.path.join(self.model_dir, "tokenizer.pkl")

        if not (os.path.exists(encoder_path) and os.path.exists(tokenizer_path)):
            return

        try:
            from keras.models import load_model

            self.encoder = load_model(encoder_path, safe_mode=False)
            with open(tokenizer_path, "rb") as file:
                self.tokenizer = pickle.load(file)
        except Exception as exc:
            self.encoder = None
            self.tokenizer = None
            self.load_error = str(exc)

    @property
    def using_trained_model(self):
        return self.encoder is not None and self.tokenizer is not None

    def embed_texts(self, texts):
        if not texts:
            return np.empty((0, self.fallback_dim), dtype=np.float32)

        if self.using_trained_model:
            from keras.preprocessing.sequence import pad_sequences

            sequences = self.tokenizer.texts_to_sequences(texts)
            padded = pad_sequences(sequences, maxlen=self.max_length, padding="post", truncating="post")
            vectors = self.encoder.predict(padded, verbose=0)
            return normalize(vectors)

        return normalize(np.vstack([self._hash_embedding(text) for text in texts]))

    def _hash_embedding(self, text):
        vector = np.zeros(self.fallback_dim, dtype=np.float32)
        for token in re.findall(r"[a-zA-Z0-9]+", text.lower()):
            digest = hashlib.md5(token.encode("utf-8")).hexdigest()
            index = int(digest[:8], 16) % self.fallback_dim
            vector[index] += 1.0
        return vector
