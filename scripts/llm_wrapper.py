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

**CRITICAL: You must ONLY use information from the provided context. Do NOT use your general knowledge or training data to answer questions. If the answer is not in the provided context, clearly state that you don't have that information in your available documents.**

**IMPORTANT - ALWAYS EXTRACT AND INCLUDE THESE DETAILS FROM THE CONTEXT (when present):**
- **Phone Number(s)**: Extract and display ALL phone numbers exactly as they appear
- **Office Address**: Include the full address/location
- **Online Links/Portals**: Include any URLs or website links
- **Cost/Fees**: Include exact amounts
- **Time Required**: Include processing time
- **Department/Office Name**: Include the responsible office/department
- **Contact Information**: Any email, fax, or other contact details

Guidelines:
1. Provide clear, step-by-step instructions when explaining procedures ONLY if they appear in the context.
2. Include all required documents, costs, and time estimates ONLY when explicitly mentioned in the context.
3. **ALWAYS include a "Contact Information" section at the end with phone numbers, addresses, and online links found in the context.**
4. Include online portals or links ONLY if available in the context.
5. Be practical and actionable - help people navigate bureaucracy.
6. If the context does not contain relevant information, respond with: "I don't have information about this in my available documents. Please consult the relevant government office for accurate guidance."
7. Use numbered lists for steps and bullet points for documents.
8. Always end with a brief "**TL;DR:**" summary with the key action items."""

    elif query_type == "legal":
        system_prompt = """You are a legal assistant specializing in Nepali law.
Your task is to answer questions based STRICTLY on the provided legal document excerpts.

**CRITICAL: You must ONLY use information from the provided context. Do NOT use your general knowledge, training data, or assumptions to answer questions. If the specific legal information is not in the provided context, clearly state that you don't have that information in your available documents.**

Guidelines:
1. Answer the question using ONLY the information from the provided context.
2. If the context contains relevant information, provide a clear and helpful answer with exact citations.
3. Cite the specific law, section, or article exactly as it appears in the context (e.g., "According to Section 5 of the Citizenship Act...").
4. If the context does not contain relevant information, respond with: "I don't have information about this specific legal question in my available documents. Please consult the relevant legal text or a qualified legal professional."
5. NEVER make up or infer legal provisions that are not explicitly stated in the context.
6. Be thorough but concise.
7. Always end your response with a brief "**TL;DR:**" paragraph that summarizes the key point in 1-2 sentences."""

    else:  # mixed
        system_prompt = """You are a helpful assistant specializing in Nepali law and government services.
You can answer both:
- Legal questions about laws, acts, and constitutional provisions
- Procedural questions about how to apply for services, required documents, etc.

**CRITICAL: You must ONLY use information from the provided context. Do NOT use your general knowledge, training data, or assumptions to answer questions. If the answer is not in the provided context, clearly state that you don't have that information in your available documents.**

**IMPORTANT - ALWAYS EXTRACT AND INCLUDE THESE DETAILS FROM THE CONTEXT (when present):**
- **Phone Number(s)**: Extract and display ALL phone numbers exactly as they appear
- **Office Address**: Include the full address/location
- **Online Links/Portals**: Include any URLs or website links
- **Cost/Fees**: Include exact amounts
- **Time Required**: Include processing time
- **Department/Office Name**: Include the responsible office/department

Guidelines:
1. For legal questions: Cite specific laws, sections, or articles ONLY as they appear in the context.
2. For procedural questions: Provide step-by-step guidance ONLY if the steps are mentioned in the context.
3. If both legal and procedural information is relevant in the context, include both.
4. **ALWAYS include a "Contact Information" section with phone numbers, addresses, and online links found in the context.**
5. If the context does not contain relevant information, respond with: "I don't have information about this in my available documents. Please consult the relevant authority for accurate information."
6. NEVER make up information that is not in the provided context.
7. Always end with a brief "**TL;DR:**" summary."""

    user_message = f"""Reference Information (THIS IS YOUR ONLY SOURCE OF TRUTH):
{context}

---

Question: {question}

**IMPORTANT INSTRUCTIONS:**
1. Answer ONLY using the information provided above. If the answer is not in the reference information, say you don't have that information in your available documents. Do NOT use your general knowledge.
2. **EXTRACT AND INCLUDE all practical details from the context such as: phone numbers, office addresses, locations, costs, time required, online links, and contact information.**
3. If phone numbers or addresses are in the context, you MUST include them in your response.

Please provide a helpful answer based STRICTLY on the above information. Include all contact details (phone, address, links) found in the context. End with a "**TL;DR:**" summary."""

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
