import os
import pickle

import numpy as np
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer

from siamese_model import build_siamese_model


MAX_LENGTH = 80
VOCAB_SIZE = 12000
MODEL_DIR = os.path.join(os.path.dirname(__file__), "saved_model")


TRAINING_PAIRS = [
    ("What is machine learning?", "Machine learning is a field of artificial intelligence where systems learn patterns from data.", 1),
    ("Define supervised learning.", "Supervised learning trains a model using labeled examples with known outputs.", 1),
    ("What is unsupervised learning?", "Unsupervised learning finds hidden patterns in data without labeled target values.", 1),
    ("What is deep learning?", "Deep learning uses neural networks with many layers to learn complex representations.", 1),
    ("What is a neural network?", "A neural network is a model made of connected layers that transform inputs into predictions.", 1),
    ("What is deadlock?", "A deadlock occurs when processes wait forever for resources held by each other.", 1),
    ("How can deadlock be prevented?", "Deadlock prevention removes at least one necessary deadlock condition such as circular wait.", 1),
    ("What is paging?", "Paging divides memory into fixed-size pages and frames for efficient memory management.", 1),
    ("What is SQL?", "SQL is a language used to query and manage relational databases.", 1),
    ("What is normalization?", "Database normalization organizes tables to reduce redundancy and improve data integrity.", 1),
    ("What is photosynthesis?", "The operating system schedules processes to share CPU time.", 0),
    ("Explain database keys.", "A neural network learns document similarity using dense vector embeddings.", 0),
    ("What is paging?", "Supervised learning uses labeled examples for training machine learning models.", 0),
    ("Define deadlock.", "SQL queries are used to retrieve records from relational databases.", 0),
    ("What is deep learning?", "Paging maps virtual memory pages to physical memory frames.", 0),
]


def tokenize_pairs(pairs):
    tokenizer = Tokenizer(num_words=VOCAB_SIZE, oov_token="<UNK>")
    tokenizer.fit_on_texts([text for pair in pairs for text in pair[:2]])

    questions = pad_sequences(tokenizer.texts_to_sequences([pair[0] for pair in pairs]), maxlen=MAX_LENGTH, padding="post")
    chunks = pad_sequences(tokenizer.texts_to_sequences([pair[1] for pair in pairs]), maxlen=MAX_LENGTH, padding="post")
    labels = np.array([pair[2] for pair in pairs], dtype=np.float32)
    return tokenizer, questions, chunks, labels


def main():
    os.makedirs(MODEL_DIR, exist_ok=True)
    tokenizer, questions, chunks, labels = tokenize_pairs(TRAINING_PAIRS)

    model, encoder = build_siamese_model(vocab_size=VOCAB_SIZE, max_length=MAX_LENGTH)
    model.fit([questions, chunks], labels, epochs=30, batch_size=4, validation_split=0.2, verbose=1)

    encoder.save(os.path.join(MODEL_DIR, "encoder.keras"))
    model.save(os.path.join(MODEL_DIR, "siamese_model.keras"))
    with open(os.path.join(MODEL_DIR, "tokenizer.pkl"), "wb") as file:
        pickle.dump(tokenizer, file)

    print(f"Saved model and tokenizer to {MODEL_DIR}")


if __name__ == "__main__":
    main()
