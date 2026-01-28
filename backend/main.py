"""
FastAPI backend for Nepal Legal AI
Provides REST API endpoints for the React frontend
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Ensure we can import from scripts/
ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.append(str(SCRIPTS))

# Load .env
load_dotenv(ROOT / ".env")

from embedding import EmbeddingModel, DEFAULT_EMBEDDING_MODEL
from llm_wrapper import generate_answer, DEFAULT_LLM_MODEL
from vector import FaissVectorStore

# Initialize FastAPI app
app = FastAPI(
    title="Nepal Legal AI API",
    description="API for searching and answering questions about Nepali legal documents",
    version="1.0.0"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3001", "http://127.0.0.1:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global resources
model: Optional[EmbeddingModel] = None
store: Optional[FaissVectorStore] = None


class SearchRequest(BaseModel):
    question: str
    top_k: int = 8
    use_llm: bool = True
    llm_model: str = DEFAULT_LLM_MODEL


class SearchResponse(BaseModel):
    answer: str
    sources: str


@app.on_event("startup")
async def startup_event():
    """Load embedding model and FAISS store on startup."""
    global model, store
    
    print("Loading embedding model...")
    model = EmbeddingModel()
    
    print("Loading FAISS vector store...")
    # Use absolute paths from project root
    index_path = ROOT / "database" / "legal_faiss.index"
    metadata_path = ROOT / "database" / "legal_faiss_meta.json"
    
    store = FaissVectorStore(
        index_path=index_path,
        metadata_path=metadata_path
    )
    
    if index_path.exists() and metadata_path.exists():
        store.load()
        print(f"FAISS index loaded successfully! ({len(store.metadata)} chunks)")
    else:
        print("Building FAISS index from processed documents...")
        store.build(processed_dir=ROOT / "dataset" / "processed", embedding_model=model)
        print("FAISS index built successfully!")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "store_loaded": store is not None
    }


@app.post("/api/search", response_model=SearchResponse)
async def search_and_answer(request: SearchRequest):
    """Search FAISS and optionally generate LLM answer."""
    if model is None or store is None:
        raise HTTPException(status_code=503, detail="Resources not loaded yet")
    
    try:
        # Search FAISS
        hits = store.search(request.question, embedding_model=model, top_k=request.top_k)
        
        # Build sources text
        sources_text = ""
        for i, hit in enumerate(hits, 1):
            meta = hit.get("metadata", {})
            source = meta.get("filename", meta.get("title", "Unknown"))
            year = meta.get("year", "")
            text_preview = hit["text"][:400] + "..." if len(hit["text"]) > 400 else hit["text"]
            sources_text += f"\n\n**{i}. {source}** ({year})\n> {text_preview}"
        
        if request.use_llm:
            try:
                context = [h["text"] for h in hits]
                answer = generate_answer(request.question, context, model=request.llm_model)
                return SearchResponse(answer=answer, sources=sources_text)
            except Exception as e:
                return SearchResponse(
                    answer=f"⚠️ Error generating response: {e}",
                    sources=sources_text
                )
        else:
            return SearchResponse(
                answer="Here are the relevant sources I found:",
                sources=sources_text
            )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
