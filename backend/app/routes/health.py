"""
Health check and status endpoints.
Provides system status, index statistics, and health monitoring.
"""

import logging
from datetime import datetime
from fastapi import APIRouter, Depends

from app.core.config import settings
from app.models.schemas import HealthResponse
from app.services.rag_service import RAGService

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Health & Status"])


def get_rag_service() -> RAGService:
    """Dependency injection for RAG service."""
    return RAGService()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Check if the API is running and get basic status"
)
async def health_check(
    rag_service: RAGService = Depends(get_rag_service)
):
    """
    Get the health status of the API.
    
    Returns:
    - Service status
    - API version
    - FAISS index status
    - Number of indexed documents
    """
    stats = rag_service.get_index_stats()
    
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        version=settings.APP_VERSION,
        index_loaded=stats["total_chunks"] > 0,
        total_documents=stats["total_documents"]
    )


@router.get(
    "/stats",
    summary="Get index statistics",
    description="Get detailed statistics about the indexed documents"
)
async def get_stats(
    rag_service: RAGService = Depends(get_rag_service)
):
    """
    Get detailed statistics about the FAISS index.
    
    Returns:
    - Total documents indexed
    - Total chunks in index
    - List of document names
    - Embedding dimension
    - LLM status
    """
    stats = rag_service.get_index_stats()
    
    return {
        "status": "ok",
        "statistics": {
            "total_documents": stats["total_documents"],
            "total_chunks": stats["total_chunks"],
            "documents": stats["documents"],
            "embedding_dimension": stats["embedding_dimension"],
            "llm_loaded": stats["llm_loaded"]
        },
        "config": {
            "chunk_size": settings.CHUNK_SIZE,
            "chunk_overlap": settings.CHUNK_OVERLAP,
            "top_k_default": settings.TOP_K_RESULTS,
            "embedding_model": settings.EMBEDDING_MODEL,
            "llm_model": settings.LLM_MODEL
        }
    }


@router.get(
    "/",
    summary="Root endpoint",
    description="Welcome message and API info"
)
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": "RAG-based legal document Q&A API for Nepali laws",
        "docs": "/docs",
        "health": "/health"
    }
