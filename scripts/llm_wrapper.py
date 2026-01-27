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
    
    context = "\n\n---\n\n".join(context_chunks)
    
    # Dynamic system prompt based on query type
    if query_type == "navigation":
        system_prompt = """You are a helpful government services assistant for Nepal.
Your task is to guide users through government procedures, services, and processes.

Guidelines:
1. Provide clear, step-by-step instructions when explaining procedures.
2. Include all required documents, costs, and time estimates when available.
3. Mention the relevant office, department, and contact information.
4. Include online portals or links if available.
5. Be practical and actionable - help people navigate bureaucracy.
6. If information is incomplete, mention what's available and suggest contacting the relevant office.
7. Use numbered lists for steps and bullet points for documents.
8. Always end with a brief "**TL;DR:**" summary with the key action items."""

    elif query_type == "legal":
        system_prompt = """You are a legal assistant specializing in Nepali law.
Your task is to answer questions based on the provided legal document excerpts.

Guidelines:
1. Answer the question using the information from the provided context.
2. If the context contains relevant information, provide a clear and helpful answer.
3. Cite the specific law, section, or article when possible (e.g., "According to Section 5 of the Citizenship Act...").
4. If the context is partially relevant, explain what you found and what might be missing.
5. Only say "I don't have enough information" if the context truly contains nothing relevant to the question.
6. Be thorough but concise.
7. Always end your response with a brief "**TL;DR:**" paragraph that summarizes the key point in 1-2 sentences."""

    else:  # mixed
        system_prompt = """You are a helpful assistant specializing in Nepali law and government services.
You can answer both:
- Legal questions about laws, acts, and constitutional provisions
- Procedural questions about how to apply for services, required documents, etc.

Guidelines:
1. For legal questions: Cite specific laws, sections, or articles when possible.
2. For procedural questions: Provide step-by-step guidance with required documents and costs.
3. If both legal and procedural information is relevant, include both.
4. Include contact information and office addresses when available.
5. Be thorough but practical - help people understand and take action.
6. Always end with a brief "**TL;DR:**" summary."""

    user_message = f"""Reference Information:
{context}

---

Question: {question}

Please provide a helpful answer based on the above information. End with a "**TL;DR:**" summary."""

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
