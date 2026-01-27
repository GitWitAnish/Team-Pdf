# FAISS vector store utilities 
# Supports both legal documents and navigation data


from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Tuple

import faiss
import numpy as np

from embedding import EmbeddingModel


class FaissVectorStore:
    # Simple FAISS store with metadata lookup.
    # Supports legal documents + navigation service data.

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
        navigation_dir: str | Path | None = "dataset/navigation",
        embedding_model: EmbeddingModel | None = None,
        include_navigation: bool = True,
    ) -> None:
        embedding_model = embedding_model or EmbeddingModel()
        
        # Load legal documents
        texts, metadatas = _load_texts_and_metadata(str(processed_dir))
        print(f"📚 Loaded {len(texts)} legal document chunks")
        
        # Load navigation data if enabled
        if include_navigation and navigation_dir:
            nav_texts, nav_metas = _load_navigation_data(str(navigation_dir))
            if nav_texts:
                texts.extend(nav_texts)
                metadatas.extend(nav_metas)
                print(f" Loaded {len(nav_texts)} navigation service chunks")
        
        print(f" Total chunks to embed: {len(texts)}")

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
        print(f" Built FAISS index with {len(self.metadata)} total entries")

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
        min_score: float = 0.3,
    ) -> List[Dict]:
        if self.index is None:
            self.load()
        if self.index is None:
            raise RuntimeError("Index failed to load")

        embedding_model = embedding_model or EmbeddingModel()
        query_emb = embedding_model.embed([query]).astype(np.float32)
        if not embedding_model.normalize:
            faiss.normalize_L2(query_emb)

        # Fetch more candidates to filter by score
        scores, idxs = self.index.search(query_emb, top_k * 2)
        results: List[Dict] = []
        for score, idx in zip(scores[0], idxs[0]):
            if idx < 0 or idx >= len(self.metadata):
                continue
            # Filter out low similarity scores
            if float(score) < min_score:
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
            # Stop once we have enough good results
            if len(results) >= top_k:
                break
        return results


def _load_texts_and_metadata(processed_dir: str) -> Tuple[List[str], List[Dict]]:
    # Load texts and metadata directly from *_chunks.json files.
    processed_path = Path(processed_dir)
    chunk_files = sorted(processed_path.glob("*_chunks.json"))
    
    # Exclude navigation chunks (handled separately)
    chunk_files = [f for f in chunk_files if "navigation" not in f.name.lower()]
    
    if not chunk_files:
        raise FileNotFoundError(f"No chunk files found in {processed_path}")

    texts: List[str] = []
    metadatas: List[Dict] = []

    for chunk_file in chunk_files:
        with open(chunk_file, encoding="utf-8") as f:
            data = json.load(f)
        for chunk in data.get("chunks", []):
            texts.append(chunk)
            meta = data.get("metadata", {}).copy()
            meta["type"] = "legal"  # Mark as legal document
            metadatas.append(meta)

    return texts, metadatas


def _load_navigation_data(navigation_dir: str) -> Tuple[List[str], List[Dict]]:
    nav_path = Path(navigation_dir)
    nav_file = nav_path / "navigation_data.json"
    
    if not nav_file.exists():
        print(f"⚠️ Navigation data not found at {nav_file}")
        return [], []
    
    try:
        # Import the navigation processor
        from navigation_processor import process_navigation_data
        texts, metadatas = process_navigation_data()
        return texts, metadatas
    except ImportError:
        # Fallback: basic processing if processor not available
        print("Navigation processor not found")
        return _basic_navigation_load(nav_file)


def _basic_navigation_load(nav_file: Path) -> Tuple[List[str], List[Dict]]:
    with open(nav_file, encoding="utf-8") as f:
        data = json.load(f)
    
    texts = []
    metadatas = []
    
    for service in data.get("services", []):
        # Create a simple text representation
        parts = [
            f"Service: {service.get('service_name', '')}",
            f"Category: {service.get('category', '')}",
            f"Description: {service.get('description', '')}",
            f"Department: {service.get('department', '')}",
        ]
        
        if service.get('steps'):
            parts.append("Steps: " + " | ".join(service['steps']))
        
        if service.get('documents_required'):
            docs = service['documents_required']
            if isinstance(docs, list):
                parts.append("Documents: " + ", ".join(docs))
        
        text = "\n".join(parts)
        texts.append(text)
        
        metadatas.append({
            "type": "navigation",
            "service_name": service.get("service_name", ""),
            "category": service.get("category", ""),
            "filename": "navigation_data.json",
            "title": service.get("service_name", ""),
        })
    
    return texts, metadatas


__all__ = ["FaissVectorStore"]


if __name__ == "__main__":
    # Building FAISS vector store
    store = FaissVectorStore()
    store.build()
  