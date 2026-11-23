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