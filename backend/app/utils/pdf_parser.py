"""
PDF parsing utility for extracting text from PDF documents.
Supports multiple PDF parsing libraries with fallback options.
"""

import logging
from pathlib import Path
from typing import Optional
import fitz  # PyMuPDF - fast and reliable PDF parsing

logger = logging.getLogger(__name__)


class PDFParser:
    """
    Handles PDF text extraction with support for various document types.
    Uses PyMuPDF (fitz) as the primary parsing engine.
    """
    
    @staticmethod
    def extract_text(file_path: Path) -> str:
        """
        Extract all text content from a PDF file.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Extracted text as a single string
            
        Raises:
            ValueError: If the file is not a valid PDF or cannot be read
        """
        if not file_path.exists():
            raise ValueError(f"File not found: {file_path}")
        
        if file_path.suffix.lower() != ".pdf":
            raise ValueError(f"Not a PDF file: {file_path}")
        
        try:
            text_content = []
            
            # Open PDF with PyMuPDF
            with fitz.open(file_path) as doc:
                logger.info(f"Processing PDF: {file_path.name} ({len(doc)} pages)")
                
                for page_num, page in enumerate(doc):
                    # Extract text from each page
                    page_text = page.get_text("text")
                    
                    if page_text.strip():
                        text_content.append(page_text)
                    
                    # Log progress for large documents
                    if (page_num + 1) % 50 == 0:
                        logger.debug(f"Processed {page_num + 1}/{len(doc)} pages")
            
            full_text = "\n\n".join(text_content)
            logger.info(f"Extracted {len(full_text)} characters from {file_path.name}")
            
            return full_text
            
        except Exception as e:
            logger.error(f"Failed to parse PDF {file_path}: {e}")
            raise ValueError(f"Failed to extract text from PDF: {e}")
    
    @staticmethod
    def extract_text_from_bytes(content: bytes, filename: str = "document.pdf") -> str:
        """
        Extract text from PDF content provided as bytes.
        Useful for processing uploaded files directly.
        
        Args:
            content: PDF file content as bytes
            filename: Original filename for logging
            
        Returns:
            Extracted text as a single string
        """
        try:
            text_content = []
            
            # Open PDF from bytes
            with fitz.open(stream=content, filetype="pdf") as doc:
                logger.info(f"Processing PDF from bytes: {filename} ({len(doc)} pages)")
                
                for page in doc:
                    page_text = page.get_text("text")
                    if page_text.strip():
                        text_content.append(page_text)
            
            full_text = "\n\n".join(text_content)
            logger.info(f"Extracted {len(full_text)} characters from {filename}")
            
            return full_text
            
        except Exception as e:
            logger.error(f"Failed to parse PDF bytes: {e}")
            raise ValueError(f"Failed to extract text from PDF: {e}")
    
    @staticmethod
    def extract_text_with_metadata(file_path: Path) -> dict:
        """
        Extract text along with document metadata.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Dictionary containing text and metadata
        """
        if not file_path.exists():
            raise ValueError(f"File not found: {file_path}")
        
        try:
            with fitz.open(file_path) as doc:
                metadata = doc.metadata
                
                text_content = []
                for page in doc:
                    page_text = page.get_text("text")
                    if page_text.strip():
                        text_content.append(page_text)
                
                return {
                    "text": "\n\n".join(text_content),
                    "metadata": {
                        "title": metadata.get("title", file_path.stem),
                        "author": metadata.get("author", "Unknown"),
                        "subject": metadata.get("subject", ""),
                        "page_count": len(doc),
                        "filename": file_path.name
                    }
                }
                
        except Exception as e:
            logger.error(f"Failed to parse PDF with metadata: {e}")
            raise ValueError(f"Failed to extract text from PDF: {e}")
