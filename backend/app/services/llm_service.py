"""
LLM service for generating answers using HuggingFace models.
Supports local LLaMA models with optimized inference.
"""

import logging
from typing import List, Optional
import torch
from transformers import (
    AutoModelForCausalLM, 
    AutoTokenizer,
    pipeline,
    BitsAndBytesConfig
)

from app.core.config import settings

logger = logging.getLogger(__name__)


class LLMService:
    """
    Handles LLM inference for answer generation.
    Implements singleton pattern for efficient model loading.
    """
    
    _instance = None
    _model = None
    _tokenizer = None
    _pipeline = None
    
    def __new__(cls):
        """Singleton pattern to ensure model is loaded only once."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the LLM."""
        if LLMService._model is None:
            self._load_model()
    
    def _load_model(self):
        """
        Load the LLaMA model with optimizations.
        Uses 4-bit quantization for memory efficiency.
        """
        try:
            logger.info(f"Loading LLM: {settings.LLM_MODEL}")
            
            # Check for GPU availability
            device = "cuda" if torch.cuda.is_available() else "cpu"
            logger.info(f"Using device: {device}")
            
            # Quantization config for memory efficiency (requires bitsandbytes)
            if device == "cuda":
                try:
                    quantization_config = BitsAndBytesConfig(
                        load_in_4bit=True,
                        bnb_4bit_compute_dtype=torch.float16,
                        bnb_4bit_use_double_quant=True,
                        bnb_4bit_quant_type="nf4"
                    )
                    
                    LLMService._tokenizer = AutoTokenizer.from_pretrained(
                        settings.LLM_MODEL,
                        trust_remote_code=True
                    )
                    
                    LLMService._model = AutoModelForCausalLM.from_pretrained(
                        settings.LLM_MODEL,
                        quantization_config=quantization_config,
                        device_map="auto",
                        trust_remote_code=True
                    )
                except ImportError:
                    logger.warning("bitsandbytes not available, loading without quantization")
                    self._load_without_quantization(device)
            else:
                self._load_without_quantization(device)
            
            # Create pipeline for easier inference
            LLMService._pipeline = pipeline(
                "text-generation",
                model=LLMService._model,
                tokenizer=LLMService._tokenizer,
                max_new_tokens=settings.LLM_MAX_NEW_TOKENS,
                temperature=settings.LLM_TEMPERATURE,
                top_p=settings.LLM_TOP_P,
                do_sample=True,
                pad_token_id=LLMService._tokenizer.eos_token_id
            )
            
            logger.info("LLM loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load LLM: {e}")
            logger.warning("Falling back to mock LLM for development")
            LLMService._model = "mock"
            LLMService._tokenizer = "mock"
    
    def _load_without_quantization(self, device: str):
        """Load model without quantization for CPU or when bitsandbytes unavailable."""
        LLMService._tokenizer = AutoTokenizer.from_pretrained(
            settings.LLM_MODEL,
            trust_remote_code=True
        )
        
        LLMService._model = AutoModelForCausalLM.from_pretrained(
            settings.LLM_MODEL,
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            device_map="auto" if device == "cuda" else None,
            trust_remote_code=True,
            low_cpu_mem_usage=True
        )
    
    def generate_answer(
        self, 
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None
    ) -> str:
        """
        Generate an answer from the given prompt.
        
        Args:
            prompt: The formatted prompt with context and question
            max_tokens: Override default max tokens
            temperature: Override default temperature
            
        Returns:
            Generated answer text
        """
        # Mock response for development without GPU
        if LLMService._model == "mock":
            return self._mock_generate(prompt)
        
        try:
            # Override generation params if provided
            gen_kwargs = {}
            if max_tokens:
                gen_kwargs["max_new_tokens"] = max_tokens
            if temperature:
                gen_kwargs["temperature"] = temperature
            
            # Generate response
            response = LLMService._pipeline(prompt, **gen_kwargs)
            
            # Extract generated text
            generated_text = response[0]["generated_text"]
            
            # Remove the prompt from the response
            if generated_text.startswith(prompt):
                answer = generated_text[len(prompt):].strip()
            else:
                answer = generated_text.strip()
            
            return answer
            
        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            return f"I apologize, but I encountered an error generating the response: {str(e)}"
    
    def _mock_generate(self, prompt: str) -> str:
        """
        Generate a mock response for development/testing.
        Useful when running without GPU or before model download.
        """
        # Extract question from prompt
        if "Question:" in prompt:
            question = prompt.split("Question:")[-1].split("\n")[0].strip()
        else:
            question = "your question"
        
        return (
            f"Based on the provided context about Nepali legal documents, "
            f"here is the answer to {question}:\n\n"
            f"This is a development response. To get actual LLM-generated answers, "
            f"please ensure you have:\n"
            f"1. A GPU with sufficient VRAM (8GB+ recommended)\n"
            f"2. The LLaMA model downloaded from HuggingFace\n"
            f"3. Proper authentication with HuggingFace (for gated models)\n\n"
            f"The context provided contains relevant information from the legal documents."
        )
    
    def build_rag_prompt(
        self, 
        question: str, 
        context_chunks: List[str],
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Build a RAG prompt with context and question.
        
        Args:
            question: User's question
            context_chunks: List of relevant text chunks
            system_prompt: Optional custom system prompt
            
        Returns:
            Formatted prompt string
        """
        if system_prompt is None:
            system_prompt = (
                "You are Nyaya.exe, an expert AI assistant specializing in Nepali laws "
                "and legal documents. Your role is to provide accurate, helpful information "
                "based on the legal context provided. Always cite your sources when possible "
                "and acknowledge if something is unclear or not covered in the provided context."
            )
        
        # Format context
        context_text = "\n\n".join([
            f"[Source {i+1}]\n{chunk}" 
            for i, chunk in enumerate(context_chunks)
        ])
        
        # Build prompt in LLaMA chat format
        prompt = f"""<s>[INST] <<SYS>>
{system_prompt}
<</SYS>>

Context from Nepali Legal Documents:
{context_text}

Based on the above context, please answer the following question. If the answer cannot be found in the context, say so clearly.

Question: {question}
[/INST]

Answer:"""
        
        return prompt
    
    def is_loaded(self) -> bool:
        """Check if the LLM is properly loaded."""
        return LLMService._model is not None
