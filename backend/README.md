# Nyaya.exe Backend API

A production-style RAG (Retrieval-Augmented Generation) API for querying Nepali legal documents.

## 📁 Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI entry point
│   ├── routes/              # API endpoints
│   │   ├── upload.py        # Document upload endpoint
│   │   ├── ask.py           # Question answering endpoint
│   │   └── health.py        # Health check endpoints
│   ├── services/            # Business logic
│   │   ├── rag_service.py   # RAG orchestration
│   │   ├── embedding_service.py  # Text embeddings
│   │   └── llm_service.py   # LLM inference
│   ├── models/              # Pydantic schemas
│   │   └── schemas.py       # Request/Response models
│   ├── core/                # Configuration
│   │   └── config.py        # Settings management
│   ├── utils/               # Utilities
│   │   ├── pdf_parser.py    # PDF text extraction
│   │   └── text_chunker.py  # Text chunking
│   └── db/                  # Vector store
│       └── faiss_store.py   # FAISS index management
├── data/                    # Stored documents & index
├── requirements.txt
└── .env.example
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your settings
```

### 3. Run the Server

```bash
# From backend directory
python -m app.main

# Or with uvicorn directly
uvicorn app.main:app --reload --port 8000
```

### 4. Access API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📡 API Endpoints

### Upload Document

```bash
POST /upload
Content-Type: multipart/form-data

curl -X POST "http://localhost:8000/upload" \
  -F "file=@document.pdf"
```

### Ask Question

```bash
POST /ask
Content-Type: application/json

curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "What are fundamental rights in Nepal?", "top_k": 5}'
```

### Health Check

```bash
GET /health
GET /stats
```

## 🔧 Configuration

Key settings in `.env`:

| Variable          | Description                 | Default                                  |
| ----------------- | --------------------------- | ---------------------------------------- |
| `EMBEDDING_MODEL` | HuggingFace embedding model | `sentence-transformers/all-MiniLM-L6-v2` |
| `LLM_MODEL`       | LLaMA model for generation  | `meta-llama/Llama-2-7b-chat-hf`          |
| `CHUNK_SIZE`      | Characters per chunk        | `500`                                    |
| `CHUNK_OVERLAP`   | Overlap between chunks      | `50`                                     |
| `TOP_K_RESULTS`   | Default search results      | `5`                                      |

## 🧠 How It Works

1. **Upload**: PDF → Extract Text → Chunk → Embed → Store in FAISS
2. **Query**: Question → Embed → Search FAISS → Build Prompt → LLM → Answer

## 📝 Notes

- For GPU acceleration, install `faiss-gpu` instead of `faiss-cpu`
- LLaMA models require HuggingFace authentication
- The system falls back to mock responses without GPU/LLM
