# LLM wrapper for answering questions with retrieved context.

from __future__ import annotations

import os
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load .env from project root
_ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(_ENV_PATH)

DEFAULT_LLM_MODEL = os.getenv("LLM_MODEL", "meta-llama/Llama-3.1-8B-Instruct")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")


def generate_answer(
    question: str,
    context_chunks: List[str],
    model: str | None = None,
    max_tokens: int = 512,
    temperature: float = 0.3,
) -> str:

    # HuggingFace Inference API call 

    api_key = HUGGINGFACE_API_KEY
    if not api_key:
        raise RuntimeError("api key not found")

    model = model or DEFAULT_LLM_MODEL
    client = InferenceClient(token=api_key)

    context = "\n\n---\n\n".join(context_chunks)
    system_prompt = """You are a legal assistant specializing in Nepali law.
Your task is to answer questions based on the provided legal document excerpts.

Guidelines:
1. Answer the question using the information from the provided context.
2. If the context contains relevant information, provide a clear and helpful answer.
3. Cite the specific law, section, or article when possible (e.g., "According to Section 5 of the Citizenship Act...").
4. If the context is partially relevant, explain what you found and what might be missing.
5. Only say "I don't have enough information" if the context truly contains nothing relevant to the question.
6. Be thorough but concise.
7. Always end your response with a brief "**TL;DR :**" paragraph that summarizes the key point in 1-2 sentences."""

    user_message = f"""Legal Document Excerpts:
{context}

---

Question: {question}

Please provide a helpful answer based on the above legal excerpts. End with an "TL;DR :" summary."""

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


__all__ = ["generate_answer", "DEFAULT_LLM_MODEL"]
