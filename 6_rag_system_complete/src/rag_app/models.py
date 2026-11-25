"""Typed data models shared by the RAG pipeline."""

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class Document:
    """A normalized source document and its metadata."""

    document_id: str
    source: str
    content_hash: str
    title: str
    version: str | None
    date: str
    text: str


@dataclass(frozen=True)
class Chunk:
    """A text segment associated with its originating document."""

    chunk_id: str
    document_id: str
    source: str
    title: str
    version: str | None
    date: str
    text: str
    embedding: list[float] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the chunk to a JSON-compatible dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "Chunk":
        """Build a chunk from a JSON-compatible dictionary."""
        return cls(**payload)


@dataclass(frozen=True)
class SearchResult:
    """A retrieved chunk and its similarity score."""

    chunk: Chunk
    score: float
    