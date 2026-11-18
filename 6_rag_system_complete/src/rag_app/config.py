
"""Application configuration and default paths."""

from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Settings:
    """Immutable settings for indexing and retrieval."""

    data_dir: Path = Path("data")
    index_path: Path = Path("storage/index.json")
    cache_path: Path = Path("storage/embedding_cache.json")
    embedding_provider: str = "hash"
    embedding_model: str = "gemini-embedding-2"
    embedding_dimension: int = 768
    chunk_max_chars: int = 240
    default_top_k: int = 3
    allowed_extensions: tuple[str, ...] = (".txt", ".md")
    required_metadata: tuple[str, ...] = ("title", "date")

    def validate(self) -> None:
        """Validate configuration values before running the pipeline."""
        if self.embedding_dimension <= 0:
            raise ValueError("embedding_dimension must be greater than zero")
        if self.chunk_max_chars <= 0:
            raise ValueError("chunk_max_chars must be greater than zero")
        if self.default_top_k <= 0:
            raise ValueError("default_top_k must be greater than zero")
        if self.embedding_provider not in ("hash", "gemini"):
            raise ValueError("embedding_provider must be 'hash' or 'gemini'")
        if not self.allowed_extensions:
            raise ValueError("allowed_extensions cannot be empty")