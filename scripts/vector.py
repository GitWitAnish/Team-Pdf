# FAISS vector store utilities 


from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Tuple

import faiss
import numpy as np

from embedding import EmbeddingModel


class FaissVectorStore:
    # Simple FAISS store with metadata lookup.

    def __init__(
        self,
        index_path: Path | str = Path("database/legal_faiss.index"),
        metadata_path: Path | str = Path("database/legal_faiss_meta.json"),
    ) -> None:
        self.index_path = Path(index_path)
        self.metadata_path = Path(metadata_path)
        self.index: faiss.Index | None = None
        self.metadata: List[Dict] = []

    def build(
        self,
        processed_dir: str | Path = "dataset/processed",
        embedding_model: EmbeddingModel | None = None,
    ) -> None:
        embedding_model = embedding_model or EmbeddingModel()
        texts, metadatas = _load_texts_and_metadata(str(processed_dir))

        embeddings = embedding_model.embed(texts)
        if not embedding_model.normalize:
            faiss.normalize_L2(embeddings)

        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(embeddings)

        # Persist metadata aligned by vector id
        self.metadata = [
            {"id": idx, "text": text, "metadata": meta}
            for idx, (text, meta) in enumerate(zip(texts, metadatas))
        ]

        self.save()

    def save(self) -> None:
        if self.index is None:
            raise RuntimeError("Index not built or loaded")
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        self.metadata_path.parent.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(self.index_path))
        self.metadata_path.write_text(json.dumps(self.metadata, ensure_ascii=False, indent=2), encoding="utf-8")

    def load(self) -> None:
        if not self.index_path.exists():
            raise FileNotFoundError(f"FAISS index not found at {self.index_path}")
        if not self.metadata_path.exists():
            raise FileNotFoundError(f"Metadata file not found at {self.metadata_path}")
        self.index = faiss.read_index(str(self.index_path))
        self.metadata = json.loads(self.metadata_path.read_text(encoding="utf-8"))

    def search(
        self,
        query: str,
        embedding_model: EmbeddingModel | None = None,
        top_k: int = 5,
    ) -> List[Dict]:
        if self.index is None:
            self.load()
        if self.index is None:
            raise RuntimeError("Index failed to load")

        embedding_model = embedding_model or EmbeddingModel()
        query_emb = embedding_model.embed([query]).astype(np.float32)
        if not embedding_model.normalize:
            faiss.normalize_L2(query_emb)

        scores, idxs = self.index.search(query_emb, top_k)
        results: List[Dict] = []
        for score, idx in zip(scores[0], idxs[0]):
            if idx < 0 or idx >= len(self.metadata):
                continue
            meta_entry = self.metadata[idx]
            results.append(
                {
                    "score": float(score),
                    "text": meta_entry["text"],
                    "metadata": meta_entry["metadata"],
                    "id": meta_entry["id"],
                }
            )
        return results


def _load_texts_and_metadata(processed_dir: str) -> Tuple[List[str], List[Dict]]:
    # Load texts and metadata directly from *_chunks.json files.
    processed_path = Path(processed_dir)
    chunk_files = sorted(processed_path.glob("*_chunks.json"))
    if not chunk_files:
        raise FileNotFoundError(f"No chunk files found in {processed_path}")

    texts: List[str] = []
    metadatas: List[Dict] = []

    for chunk_file in chunk_files:
        with open(chunk_file, encoding="utf-8") as f:
            data = json.load(f)
        for chunk in data.get("chunks", []):
            texts.append(chunk)
            metadatas.append(data.get("metadata", {}))

    return texts, metadatas


__all__ = ["FaissVectorStore"]


if __name__ == "__main__":
    # Building FAISS vector store
    store = FaissVectorStore()
    store.build()
  