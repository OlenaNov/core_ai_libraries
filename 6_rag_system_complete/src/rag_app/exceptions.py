"""Application-specific exceptions."""


class DocumentProcessingError(Exception):
    """Raised when a source document cannot be processed."""


class IndexPersistanceError(Exception):
    """Raised when the index cannot be saved or loaded."""


class RetievalError(Exception):
    """Raised when a retrieval operation cannot be completed."""


class EmbeddingError(Exception):
    """Raised when an embedding provider or cache operation fails."""
    