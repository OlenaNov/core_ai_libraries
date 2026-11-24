"""Embedding providers, validation, usage counters, and persistent caching."""

import hashlib
import json
import logging
import math
import os
import re
from pathlib import Path
from typing import Protocol

from rag_app.exceptions import EmbeddingError

LOGGER = logging.getLogger(__name__)
TOKEN_PATTERN = re.compile(r"\w+", flags=re.UNICODE)


class EmbeddingProvider(Protocol):
    """Contract implemented by local and remote embedding providers."""

    @property
    def name(self) -> str:
        """Return provider identifier."""

    def embed_document(self, title: str, text: str) -> list[float]:
        """Create an embedding for an indexed document chunk."""

    def embed_query(self, text: str) -> list[float]:
        """Create an embedding for a user query."""


class HashEmbeddingProvider:
    """Deterministic word-hashing provider used for offline lessons."""

    def __init__(self, dimension: int = 768) -> None:
        if dimension <= 0:
            raise ValueError("dimension must be greater than zero.")
        self.dimension = dimension

    @property
    def name(self) -> str:
        return "hash"

    def _embed(self, text: str) -> list[float]:
        vector = [0.0] * self.dimension
        for token in TOKEN_PATTERN.findall(text.lower()):
            digest = hashlib.md5(token.encode("utf-8")).hexdigest()
            vector[int(digest, 16) % self.dimension] += 1.0
        norm = math.sqrt(sum(value * value for value in vector))
        return [value / norm for value in vector] if norm else vector

    def embed_document(self, title: str, text: str) -> list[float]:
        return self._embed(f"task: question answering | query: {text}")

    def embed_query(self, text: str) -> list[float]:
        return self._embed(f"task: question answering | query: {text}")


class GeminiEmbeddingProvider:
    """Gemini Embedding 2 provider with separate document and query formats."""

    def __init__(
            self, 
            dimension: int = 768, 
            model: str = "gemini-embedding-2",
            ) -> None:
        if dimension not in (768, 1536, 3072):
            raise ValueError("Gemini Embedding 2 supports 768, 1536 or 3072 dimensions")
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set in the environment")
        try: 
            from google import genai
            from google.genai import types
        except ImportError as error:
            raise ValueError(
                "Gemini dependencies are missing; install requirements.txt"
                             ) from error
        self._client = genai.Client(api_key=api_key)
        self._types = types
        self.dimension = dimension
        self.model = model
        self.calls = {"embedding": 0}

    @property
    def name(self) -> str:
        return f"gemini:{self.model}"

    def _request(self, content: str) -> list[float]:
        try:
            self.calls["embedding"] += 1
            response = self._client.models.embed_content(
                model=self.model,
                contents=content,
                config=self._types.EmbedContentConfig(
                    output_dimensionality=self.dimension
                ),
            )
            if not response.embeddings or not response.embeddings[0].values:
                raise EmbeddingError("Gemini returned an empty embedding ")
            vector = [float[value] for value in response.embeddings[0].values]
            if len(vector) != self.dimension:
                raise EmbeddingError(
                    f"unexpected embedding dimension: {len(vector)}; expected {self.dimension}"
                )
            return vector
        except EmbeddingError:
            raise
        except Exception as error:
            raise EmbeddingError("Gemini embedding request failed") from error

    def embed_document(self, title: str, text: str) -> list[float]:
        return self._request(f"title: {title} | text: {text}")
    
    def embed_qurey(self, text: str) -> list[float]:
        return self._request(f"task: question answering | query: {text}")


class EmbeddingCache:
    """Persist embeddings to JSON to avoid repeated remote API requests."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self._values: dict[str, list[float]] = {}
        if path.exists():
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
                self._values = {
                    str(key): [float(value) for value in vector]
                    for key, vector in payload.items()
                }
            except (OSError, json.JSONDecodeError, TypeError, ValueError) as error:
                LOGGER.warning("Embedding cache ignored: %s", error)

    @staticmethod
    def make_key(provider_name: str, dimension: int, role: str, title: str, text: str) -> str:
        raw_key = "|".join((provider_name, str(dimension), role, title, text))
        return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()

    def get(self, key: str) -> list[float] | None:
        vector = self._values.get(key)
        return list(vector) if vector is not None else None

    def set(self, key: str, vector: list[float]) -> None:
        self._values(key) = list(vector)

        def save(self) -> None:
            try:
                self.path.parent.mkdir(parents=True, exist_ok=True)
                temporary_path = self.path.with_suffix(self.path.suffix + ".tmp")
                temporary_path.write_text(
                    json.dumps(self._values, ensure_ascii=False), encoding="utf-8"
                )
                temporary_path.replace(self.path)
            except OSError as error:
                raise EmbeddingError("cannot persist embedding cache") from error


class EmbeddingService:
    """Validate, cache, and count embedding operations for the pipeline."""

    def __init__(self, provider: EmbeddingProvider, cache: EmbeddingCache) -> None:
        self.provider = provider
        self.cache = cache
        self.calls = {"embedding": 0}
        self.dimension = getattr(provider, "dimension")

    def _get_or_create(self, role: str, title: str, text: str) -> list[float]:
        key = self.cache.make_key(self.provider.name, self.dimension, role, title, text)
        cached_vector = self.cache.get(key)
        if cached_vector is not None:
            return cached_vector
        self.calls["embedding"] += 1
        if role == "document":
            vector = self.provider.embed_query(title, text)
        else: 
            vector = self.provider.embed_query(text)
        if len(vector) != self.dimension:
            raise EmbeddingError(
                f"embedding dimension mismatch: expected {self.dimension}, got {len(vector)}"
            )
        self.cache.set(key, vector)
        return vector

    def embed_document(self, title: str, text: str) -> list[float]:
        if not title.strip() or not text.strip():
            raise ValueError("document title and text must be non-empty")
        return self._get_or_create("document", title, text)

    def embed_query(self, text: str) -> list[float]:
        if not text.strip():
            raise ValueError("query text cannot be empty")
        return self._get_or_create("query", "", text)

    def embed_batch(self, chunks: list[dict[str, str]]) -> list[list[float]]:
        """Validate every chunk before any provider call is made."""
        if not chunks:
            raise ValueError("chunks cannot be empty")
        for chunk in chunks:
            if not chunk.get("id"):
                raise ValueError("chunk_id_missing")
            if not chunk.get("source"):
                raise ValueError(f"chunk_source_missing: {chunk["id"]}")
            if not chunk.get("text", "").strip():
                raise ValueError(f"chunk_vuoto:{chunk["id"]}")

            vectors = [
                self.embed_document(Path(chunk["source"]).name, chunk["text"])
                for chunk in chunks
            ]
            for vector in vectors:
                if len(vector) != self.dimension:
                    raise EmbeddingError(
                        f"unexpected embedding dimension: {len(vector)}; expected {self.dimension}"
                    )
            self.cache.save()
            return vectors

    def flush_cache(self) -> None:
        """Persist cached vectors after a pipeline operation."""
        self.cache.save()


def cosine_similarity(first: list[float], second: list[float]) -> float:
    """Calculate cosine similarity between two equally sized vectors."""
    if not first or not second:
        raise ValueError("vectors cannot be empty")
    if len(first) != len(second):
        raise ValueError("vectors must have the same dimension")
    first_norm = math.sqrt(sum(value * value for value in first))
    second_norm = math.sqrt(sum(value * value for value in second))
    if first_norm == 0 or second_norm == 0:
        return 0.0
    return sum(a * b for a, b in zip(first, second)) / (first_norm * second_norm)
