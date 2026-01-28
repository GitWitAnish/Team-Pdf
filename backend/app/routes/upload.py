"""
Upload endpoint for processing PDF documents.
Handles file upload, validation, and triggers document processing.
"""

import logging
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse

from app.models.schemas import UploadResponse, ErrorResponse
from app.services.rag_service import RAGService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/upload", tags=["Document Upload"])

# Dependency to get RAG service instance
def get_rag_service() -> RAGService:
    """Dependency injection for RAG service."""
    return RAGService()


@router.post(
    "",
    response_model=UploadResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid file"},
        500: {"model": ErrorResponse, "description": "Processing error"}
    },
    summary="Upload a PDF document",
    description="""
    Upload a PDF document to be processed and indexed for RAG queries.
    
    The document will be:
    1. Validated as a PDF file
    2. Text extracted from all pages
    3. Split into overlapping chunks
    4. Converted to embeddings
    5. Stored in the FAISS vector index
    
    Supported formats: PDF only (for now)
    Maximum file size: 50MB (configurable)
    """
)
async def upload_document(
    file: UploadFile = File(..., description="PDF file to upload"),
    rag_service: RAGService = Depends(get_rag_service)
):
    """
    Upload and process a PDF document for RAG indexing.
    
    - **file**: PDF file to upload and process
    
    Returns processing results including number of chunks created.
    """
    # Validate file type
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No filename provided"
        )
    
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported. Please upload a .pdf file."
        )
    
    # Validate content type
    if file.content_type and file.content_type != "application/pdf":
        logger.warning(
            f"Unexpected content type: {file.content_type} for {file.filename}"
        )
    
    try:
        # Read file content
        content = await file.read()
        
        # Validate file size (50MB max)
        max_size = 50 * 1024 * 1024  # 50MB
        if len(content) > max_size:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size is 50MB, got {len(content) / 1024 / 1024:.1f}MB"
            )
        
        # Validate it's actually a PDF (check magic bytes)
        if not content.startswith(b"%PDF"):
            raise HTTPException(
                status_code=400,
                detail="Invalid PDF file. The file does not appear to be a valid PDF."
            )
        
        logger.info(f"Processing upload: {file.filename} ({len(content)} bytes)")
        
        # Process the document
        result = await rag_service.process_document(content, file.filename)
        
        return UploadResponse(**result)
        
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Validation error processing {file.filename}: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error processing {file.filename}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process document: {str(e)}"
        )
    finally:
        await file.close()


@router.delete(
    "/{document_name}",
    summary="Delete a document",
    description="Remove a document and its chunks from the index"
)
async def delete_document(
    document_name: str,
    rag_service: RAGService = Depends(get_rag_service)
):
    """
    Delete a document from the FAISS index.
    
    - **document_name**: Name of the document to delete
    """
    try:
        deleted_count = rag_service.delete_document(document_name)
        
        if deleted_count == 0:
            raise HTTPException(
                status_code=404,
                detail=f"Document not found: {document_name}"
            )
        
        return {
            "success": True,
            "message": f"Deleted {deleted_count} chunks for {document_name}",
            "deleted_chunks": deleted_count
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting document {document_name}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete document: {str(e)}"
        )
