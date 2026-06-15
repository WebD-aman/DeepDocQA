# Document QA Chatbot

A simple document question-answering chatbot built with **React**, **Flask**, **TensorFlow/Keras**, and **NLTK**.

Upload a PDF, DOCX, or TXT file and ask questions about its content. The chatbot searches the uploaded document and returns the most relevant answer.

## Features

* Upload PDF, DOCX, and TXT files
* One active document at a time
* Automatic document text extraction and chunking
* Semantic search using a Siamese Bi-LSTM model
* Confidence score for answers
* Chat-style user interface
* Fallback mode available if the trained model is not present

## Project Structure

```text
document-qa-chatbot/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── models/
│   └── uploads/
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## Setup

### Backend

```bash
cd backend
python -m venv .venv
pip install -r requirements.txt
python app.py
```

Backend runs at:

```text
http://localhost:5000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at:

```text
http://localhost:5173
```

## Training the Model (Optional)

To use the deep learning model:

```bash
cd backend/models
python train.py
```

After training, restart the Flask server.

## API Endpoints

### Upload Document

```http
POST /upload
```

Upload a PDF, DOCX, or TXT file.

### Ask Question

```http
POST /ask
```

Request:

```json
{
  "question": "What is deadlock?"
}
```

### Check Status

```http
GET /status
```

Returns the currently active document.

## How It Works

1. Upload a document.
2. The text is extracted and divided into chunks.
3. The document chunks are converted into embeddings.
4. A user question is converted into an embedding.
5. Cosine similarity finds the most relevant chunk.
6. The best matching chunk is returned as the answer.

## Tech Stack

* Frontend: React, Vite
* Backend: Flask
* NLP: NLTK
* Deep Learning: TensorFlow / Keras
* Model: Siamese Bi-LSTM

## Notes

* Only the latest uploaded document is used for answering questions.
* Uploading a new document replaces the previous one.
* The project can run with or without the trained model.
