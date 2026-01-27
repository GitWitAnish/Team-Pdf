"""
Text chunking utility for splitting documents into smaller pieces.
Implements various chunking strategies for optimal RAG performance.
"""

import logging
import re
from typing import List, Dict, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class TextChunk:
    """Represents a chunk of text with metadata."""
    text: str
    index: int
    start_char: int
    end_char: int
    metadata: Dict[str, Any]


class TextChunker:
    """
    Splits text into overlapping chunks for embedding and retrieval.
    Uses a sliding window approach with configurable size and overlap.
    """
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        """
        Initialize the chunker with specified parameters.
        
        Args:
            chunk_size: Target size of each chunk in characters
            chunk_overlap: Number of characters to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        if chunk_overlap >= chunk_size:
            raise ValueError("Chunk overlap must be less than chunk size")
    
    def chunk_text(
        self, 
        text: str, 
        document_name: str = "unknown"
    ) -> List[TextChunk]:
        """
        Split text into overlapping chunks.
        Attempts to break at sentence boundaries when possible.
        
        Args:
            text: The text to chunk
            document_name: Name of the source document for metadata
            
        Returns:
            List of TextChunk objects
        """
        if not text or not text.strip():
            logger.warning(f"Empty text provided for chunking: {document_name}")
            return []
        
        # Clean the text
        text = self._clean_text(text)
        
        chunks = []
        start = 0
        chunk_index = 0
        
        while start < len(text):
            # Calculate end position
            end = start + self.chunk_size
            
            # If we're not at the end, try to find a good break point
            if end < len(text):
                # Look for sentence endings (., !, ?) within the last 20% of the chunk
                search_start = end - int(self.chunk_size * 0.2)
                search_text = text[search_start:end]
                
                # Find last sentence boundary
                last_break = self._find_last_sentence_break(search_text)
                
                if last_break != -1:
                    end = search_start + last_break + 1
            else:
                end = len(text)
            
            # Extract chunk text
            chunk_text = text[start:end].strip()
            
            if chunk_text:  # Only add non-empty chunks
                chunk = TextChunk(
                    text=chunk_text,
                    index=chunk_index,
                    start_char=start,
                    end_char=end,
                    metadata={
                        "document_name": document_name,
                        "chunk_index": chunk_index,
                        "char_count": len(chunk_text)
                    }
                )
                chunks.append(chunk)
                chunk_index += 1
            
            # Move start position with overlap
            start = end - self.chunk_overlap
            
            # Prevent infinite loop
            if start >= len(text) - self.chunk_overlap:
                break
        
        logger.info(
            f"Created {len(chunks)} chunks from {document_name} "
            f"(avg size: {sum(len(c.text) for c in chunks) // max(len(chunks), 1)} chars)"
        )
        
        return chunks
    
    def _clean_text(self, text: str) -> str:
        """
        Clean and normalize text for better chunking.
        
        Args:
            text: Raw text to clean
            
        Returns:
            Cleaned text
        """
        # Replace multiple newlines with double newline
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Replace multiple spaces with single space
        text = re.sub(r' {2,}', ' ', text)
        
        # Remove page numbers (common patterns)
        text = re.sub(r'\n\s*\d+\s*\n', '\n', text)
        
        # Remove excessive whitespace while preserving paragraph breaks
        lines = text.split('\n')
        cleaned_lines = [line.strip() for line in lines]
        text = '\n'.join(cleaned_lines)
        
        return text.strip()
    
    def _find_last_sentence_break(self, text: str) -> int:
        """
        Find the last sentence boundary in the text.
        
        Args:
            text: Text to search for sentence breaks
            
        Returns:
            Index of last sentence break, or -1 if not found
        """
        # Look for sentence endings followed by space or end
        matches = list(re.finditer(r'[.!?]\s', text))
        
        if matches:
            return matches[-1].start()
        
        # If no sentence break, try to break at paragraph
        newline_pos = text.rfind('\n')
        if newline_pos != -1:
            return newline_pos
        
        return -1
    
    def chunk_by_paragraphs(
        self, 
        text: str, 
        document_name: str = "unknown",
        min_chunk_size: int = 100
    ) -> List[TextChunk]:
        """
        Alternative chunking strategy that preserves paragraph boundaries.
        Combines short paragraphs until chunk_size is reached.
        
        Args:
            text: The text to chunk
            document_name: Name of the source document
            min_chunk_size: Minimum size for a chunk
            
        Returns:
            List of TextChunk objects
        """
        text = self._clean_text(text)
        paragraphs = text.split('\n\n')
        
        chunks = []
        current_chunk = []
        current_size = 0
        chunk_index = 0
        start_char = 0
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            para_size = len(para)
            
            # If adding this paragraph exceeds chunk_size, save current chunk
            if current_size + para_size > self.chunk_size and current_chunk:
                chunk_text = '\n\n'.join(current_chunk)
                chunk = TextChunk(
                    text=chunk_text,
                    index=chunk_index,
                    start_char=start_char,
                    end_char=start_char + len(chunk_text),
                    metadata={
                        "document_name": document_name,
                        "chunk_index": chunk_index,
                        "char_count": len(chunk_text)
                    }
                )
                chunks.append(chunk)
                chunk_index += 1
                start_char += len(chunk_text) + 2
                current_chunk = []
                current_size = 0
            
            current_chunk.append(para)
            current_size += para_size + 2  # +2 for paragraph separator
        
        # Don't forget the last chunk
        if current_chunk:
            chunk_text = '\n\n'.join(current_chunk)
            if len(chunk_text) >= min_chunk_size:
                chunk = TextChunk(
                    text=chunk_text,
                    index=chunk_index,
                    start_char=start_char,
                    end_char=start_char + len(chunk_text),
                    metadata={
                        "document_name": document_name,
                        "chunk_index": chunk_index,
                        "char_count": len(chunk_text)
                    }
                )
                chunks.append(chunk)
        
        logger.info(f"Created {len(chunks)} paragraph-based chunks from {document_name}")
        
        return chunks
