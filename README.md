# Deep Learning Document Question Answering System

A full-stack document QA chatbot built with React, Flask, NLTK, TensorFlow/Keras, and a Siamese Bi-LSTM sentence embedding model. The app accepts one active PDF, TXT, or DOCX document and answers questions only from the most recently uploaded document.

## Features

- Upload PDF, TXT, or DOCX files.
- Keeps only one active document at a time.
- Deletes the previous uploaded file, chunks, and embeddings when a new file is uploaded.
- Splits document text into searchable chunks.
- Embeds questions and chunks using a trained Siamese Bi-LSTM encoder when available.
- Uses cosine similarity to find the most relevant chunk.
- Returns a confidence score and a fallback message when confidence is low.
- Modern React UI with drag-and-drop upload, chat-style answers, loaders, and errors.

## Project Structure

```text
document-qa-chatbot/
  backend/
    app.py
    requirements.txt
    routes/
    services/
    models/
      siamese_model.py
      train.py
      saved_model/
    uploads/
  frontend/
    src/
      components/
      pages/
      api.js
    package.json
    vite.config.js
  README.md
```

## Backend Setup

From the project root:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python app.py
```

The backend runs at `http://localhost:5000`.

On macOS/Linux, activate the virtual environment with:

```bash
source .venv/bin/activate
```

## Frontend Setup

Open another terminal:

```bash
cd frontend
npm install
copy .env.example .env
npm run dev
```

The frontend runs at `http://localhost:5173`.

On macOS/Linux, use `cp .env.example .env`.

## Training the Siamese Bi-LSTM Model

The backend can run before training by using a lightweight hashed embedding fallback. For the deep learning version, train the included small dataset:

```bash
cd backend/models
python train.py
```

This saves:

- `backend/models/saved_model/encoder.keras`
- `backend/models/saved_model/siamese_model.keras`
- `backend/models/saved_model/tokenizer.pkl`

Restart Flask after training so the inference pipeline loads the saved encoder and tokenizer.

## API Endpoints

### `POST /upload`

Multipart form field:

- `file`: PDF, TXT, or DOCX document

Response:

```json
{
  "message": "Document uploaded and processed successfully.",
  "current_document": "OperatingSystems.pdf",
  "chunk_count": 12,
  "using_trained_model": true
}
```

### `POST /ask`

Request:

```json
{
  "question": "What is deadlock?"
}
```

Response:

```json
{
  "answer": "...",
  "confidence": 0.91,
  "source_chunk": "...",
  "timestamp": "2026-06-13T10:30:00+00:00"
}
```

### `GET /status`

Response:

```json
{
  "current_document": "OperatingSystems.pdf"
}
```

## How It Works

1. The user uploads a document.
2. The backend clears the previous upload, chunks, and embeddings.
3. Text is extracted using PyPDF2, python-docx, or normal text reading.
4. NLTK sentence tokenization creates chunks with slight sentence overlap.
5. Each chunk is converted into an embedding.
6. The user submits a question.
7. The question is embedded and compared with chunk embeddings using cosine similarity.
8. The most similar chunk is returned if its confidence is above the threshold.

## Viva Explanation Notes

- The Siamese network uses the same Bi-LSTM encoder for both the question and the document chunk.
- Shared weights make both inputs live in the same vector space.
- Cosine similarity measures how close the question meaning is to each document chunk.
- The system is document-grounded because answers are copied from the best chunk, not generated freely.
- Replacing a document resets the engine state, so the chatbot cannot answer from older documents.

## Render Deployment

### Backend on Render

1. Create a new Web Service.
2. Set the root directory to `backend`.
3. Use Python as the runtime.
4. Build command:

```bash
pip install -r requirements.txt
```

5. Start command:

```bash
python app.py
```

6. Add environment variables:

```text
PORT=10000
FRONTEND_ORIGIN=https://your-frontend-domain
MAX_UPLOAD_MB=10
```

TensorFlow can be heavy on free hosting tiers. For a student laptop demo, local execution is recommended.

### Frontend on Render

1. Create a Static Site.
2. Set the root directory to `frontend`.
3. Build command:

```bash
npm install && npm run build
```

4. Publish directory:

```text
dist
```

5. Add:

```text
VITE_API_BASE_URL=https://your-backend-domain
```

## Laptop Performance

- Default upload limit is 10 MB.
- Chunk size is limited to reduce RAM use.
- The included training data is intentionally small.
- The fallback embedding mode lets the project demo run even before training.
