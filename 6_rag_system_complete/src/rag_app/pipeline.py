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
from rag_app.generation import generate_answer
from rag_app.index_store import load_index
from rag_app.models import SearchResult
from rag_app.retrieval import retrieve

LOGGER = logging.getLogger(__name__)

# TODO