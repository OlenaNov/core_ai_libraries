"""High-level application facade for indexing and question answering."""

import logging
from pathlib import Path

from rag_app.config import Settings
from rag_app.embeddings import (
    EmbeddingCache,
    EmbeddingService,
    GeminiEmbeddingProvider,
    HashEmbeddingProvider,
)