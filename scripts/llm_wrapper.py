# LLM wrapper for answering questions with retrieved context.
# Supports both legal documents and navigation/procedural guidance.

from __future__ import annotations

import os
from pathlib import Path
from typing import List, Dict

from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load .env from project root
_ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(_ENV_PATH)

DEFAULT_LLM_MODEL = os.getenv("LLM_MODEL", "meta-llama/Llama-3.1-8B-Instruct")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")


def detect_query_type(question: str, context_chunks: List[str] = None) -> str:
    """
    Detect whether the query is about legal information or procedural navigation.
    Returns: 'legal', 'navigation', or 'mixed'
    """
    question_lower = question.lower()
    
    # Navigation indicators
    nav_keywords = [
        "how to", "how do i", "how can i", "steps to", "process for",
        "where to", "which office", "documents required", "documents needed",
        "apply for", "get a", "obtain", "register for", "registration",
        "renew", "renewal", "what documents", "how much", "cost of",
        "time required", "how long", "procedure", "kaha", "kasari",
        "office address", "phone number", "contact"
    ]
    
    # Legal indicators  
    legal_keywords = [
        "what is", "what are", "define", "definition", "according to",
        "section", "article", "act says", "law says", "provision",
        "constitutional", "legal rights", "punishment", "penalty",
        "offense", "crime", "rights", "duties", "fundamental"
    ]
    
    nav_score = sum(1 for kw in nav_keywords if kw in question_lower)
    legal_score = sum(1 for kw in legal_keywords if kw in question_lower)
    
    if nav_score > legal_score:
        return "navigation"
    elif legal_score > nav_score:
        return "legal"
    else:
        return "mixed"


def generate_answer(
    question: str,
    context_chunks: List[str],
    chunk_metadata: List[Dict] = None,
    model: str | None = None,
    max_tokens: int = 1024,
    temperature: float = 0.3,
) -> str:

    # HuggingFace Inference API call 

    api_key = HUGGINGFACE_API_KEY
    if not api_key:
        raise RuntimeError("api key not found")

    model = model or DEFAULT_LLM_MODEL
    client = InferenceClient(token=api_key)

    # Detect query type for better prompting
    query_type = detect_query_type(question, context_chunks)
    
    # Build context with source attribution
    if chunk_metadata:
        context_parts = []
        for i, (chunk, meta) in enumerate(zip(context_chunks, chunk_metadata)):
            source = meta.get("title") or meta.get("filename") or "Unknown Source"
            context_parts.append(f"[Source: {source}]\n{chunk}")
        context = "\n\n---\n\n".join(context_parts)
    else:
        context = "\n\n---\n\n".join(context_chunks)
    
    # Dynamic system prompt based on query type
    if query_type == "navigation":
        system_prompt = """You are a helpful government services assistant for Nepal.
Your task is to guide users through government procedures, services, and processes.

**CRITICAL: You must ONLY use information from the provided context. Do NOT use your general knowledge or training data. If the answer is not in the provided context, clearly state that you don't have that information in your available documents.**

Guidelines:
1. Provide clear, step-by-step instructions when explaining procedures.
2. Include all relevant details from the context (documents needed, costs, fees, time, locations, phone numbers, links, etc.) naturally in your answer.
3. Be practical and actionable - help people navigate bureaucracy.
4. If the context does not contain relevant information, say: "I don't have information about this in my available documents."
5. Use numbered lists for steps and bullet points for documents.
6. End with a brief "**TL;DR:**" summary."""

    elif query_type == "legal":
        system_prompt = """You are a legal assistant specializing in Nepali law.
Your task is to answer questions based STRICTLY on the provided legal document excerpts.

**CRITICAL: You must ONLY use information from the provided context. Do NOT use your general knowledge or training data. If the specific legal information is not in the provided context, clearly state that you don't have that information.**

Guidelines:
1. Answer the question using ONLY the information from the provided context.
2. Always cite the source document name along with section/article (e.g., "According to Section 38 of the Constitution of Nepal...").
3. If the context does not contain relevant information, say: "I don't have information about this specific legal question in my available documents."
4. NEVER make up or infer legal provisions not explicitly stated in the context.
5. Be thorough but concise.
6. End with a brief "**TL;DR:**" paragraph."""

    else:  # mixed
        system_prompt = """You are a helpful assistant specializing in Nepali law and government services.
You can answer both:
- Legal questions about laws, acts, and constitutional provisions
- Procedural questions about how to apply for services, required documents, etc.

**CRITICAL: You must ONLY use information from the provided context. Do NOT use your general knowledge or training data. If the answer is not in the provided context, clearly state that you don't have that information.**

Guidelines:
1. For legal questions: Always cite the source document name along with section/article (e.g., "According to Section 38 of the Constitution of Nepal...").
2. For procedural questions: Provide step-by-step guidance when available in the context.
3. Include all relevant details from the context naturally in your answer.
4. If the context does not contain relevant information, say: "I don't have information about this in my available documents."
5. NEVER make up information not in the provided context.
6. End with a brief "**TL;DR:**" summary."""

    user_message = f"""Reference Information:
{context}

---

Question: {question}

Answer the question using ONLY the information provided above. Include all relevant details from the context. End with a "**TL;DR:**" summary."""

    # Use chat_completion for conversational models like Llama
    response = client.chat_completion(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
    )

    return response.choices[0].message.content.strip()


__all__ = ["generate_answer", "DEFAULT_LLM_MODEL", "detect_query_type"]
