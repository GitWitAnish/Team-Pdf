# Embedding utilities for the legal RAG stack.

# Uses SentenceTransformers to produce normalized embeddings suitable for FAISS.
# Reads EMBEDDING_MODEL from .env file.

from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable, List, Union

import numpy as np
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# Load .env from project root
_ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(_ENV_PATH)

# Default embedding model from .env or fallback
DEFAULT_EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")


class EmbeddingModel:

    def __init__(
        self,
        model_name: str | None = None,
        device: str | None = None,
        normalize: bool = True,
    ) -> None:
        self.model_name = model_name or DEFAULT_EMBEDDING_MODEL
        self.normalize = normalize
        self.model = SentenceTransformer(self.model_name, device=device)

    @property
    def dimension(self) -> int:
        return self.model.get_sentence_embedding_dimension()

    def embed(self, texts: Union[str, List[str], Iterable[str]]) -> np.ndarray:
        if isinstance(texts, str):
            texts = [texts]
        embeddings = self.model.encode(
            list(texts),
            batch_size=32,
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=self.normalize,
        )
        return embeddings


__all__ = ["EmbeddingModel"]
