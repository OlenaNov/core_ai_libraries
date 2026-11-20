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

