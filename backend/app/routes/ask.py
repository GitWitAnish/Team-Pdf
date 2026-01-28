"""
Ask endpoint for RAG question-answering.
Handles user questions, retrieves relevant context, and generates answers.
"""

import logging
from fastapi import APIRouter, HTTPException, Depends

from app.models.schemas import AskRequest, AskResponse, ErrorResponse
from app.services.rag_service import RAGService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ask", tags=["Question Answering"])


def get_rag_service() -> RAGService:
    """Dependency injection for RAG service."""
    return RAGService()


@router.post(
    "",
    response_model=AskResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid request"},
        500: {"model": ErrorResponse, "description": "Processing error"}
    },
    summary="Ask a question",
    description="""
    Ask a question about the indexed legal documents.
    
    The RAG pipeline will:
    1. Convert your question to an embedding
    2. Search FAISS for the most relevant document chunks
    3. Build a context-rich prompt with the retrieved chunks
    4. Send the prompt to the LLaMA model
    5. Return the generated answer along with source citations
    
    **Tips for better results:**
    - Be specific in your questions
    - Include relevant keywords (e.g., "citizenship", "fundamental rights")
    - Ask one question at a time for clearer answers
    """
)
async def ask_question(
    request: AskRequest,
    rag_service: RAGService = Depends(get_rag_service)
):
    """
    Ask a question and get an AI-generated answer based on indexed documents.
    
    - **question**: Your question about Nepali laws/documents
    - **top_k**: Number of relevant chunks to use (default: 5)
    
    Returns the answer along with source chunks used for context.
    """
    try:
        logger.info(f"Received question: {request.question[:100]}...")
        
        # Call RAG service
        result = await rag_service.search_and_answer(
            question=request.question,
            top_k=request.top_k
        )
        
        return AskResponse(
            answer=result["answer"],
            sources=result["sources"],
            question=result["question"],
            processing_time=result["processing_time"]
        )
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error processing question: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process question: {str(e)}"
        )


@router.get(
    "/search",
    summary="Search documents (without LLM)",
    description="Search for relevant chunks without generating an LLM answer"
)
async def search_only(
    question: str,
    top_k: int = 5,
    rag_service: RAGService = Depends(get_rag_service)
):
    """
    Search for relevant document chunks without LLM generation.
    Useful for quick lookups or when you want raw context.
    
    - **question**: Search query
    - **top_k**: Number of results to return
    """
    try:
        # Get embedding and search
        query_embedding = rag_service.embedding_service.embed_query(question)
        results = rag_service.faiss_store.search(query_embedding, top_k)
        
        return {
            "query": question,
            "results": [
                {
                    "text": r["text"],
                    "document_name": r["document_name"],
                    "chunk_index": r["chunk_index"],
                    "similarity_score": round(r["similarity_score"], 4)
                }
                for r in results
            ],
            "total_results": len(results)
        }
        
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Search failed: {str(e)}"
        )
