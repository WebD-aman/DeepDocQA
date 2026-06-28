# DeepDocQA

A document question-answering app built with React, Flask, and a Siamese Bi-LSTM model.

Users can upload PDF, DOCX, or TXT files and ask questions about the uploaded document.

## Live Demo

Frontend: https://deepdocqa-frontend.onrender.com

Backend API: https://deepdocqa.onrender.com

## Setup

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
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

## Train Model

```bash
cd backend/models
python train.py
```

## Deploy on Render

Backend:

```text
Root Directory: backend
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
```

Frontend:

```text
Root Directory: frontend
Build Command: npm install && npm run build
Publish Directory: dist
```

## API

```http
POST /upload
POST /ask
GET /status
```
