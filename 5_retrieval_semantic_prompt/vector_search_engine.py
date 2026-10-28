
import hashlib
import logging 
import math
import re
from typing import Any, Dict, List, Tuple

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("VectorSearchEngine")

# Constants
DEFAULT_DIMENSION = 1024
MIN_QUERY_LENGTH = 3
MAX_QUERY_LENGTH = 500
MAX_TOKEN_LIMIT = 512

DOCUMENTS = [
    {"id": 0, "title": "Resi", "text": "Il reso è gratuito entro quattordici giorni dalla consegna."},
    {"id": 1, "title": "Rimborsi", "text": "Il rimborso arriva entro sette giorni dal ricevimento del reso."},
    {"id": 2, "title": "Spedizioni", "text": "La spedizione costa cinque euro e la consegna avviene in tre giorni."},
    {"id": 3, "title": "Pagamenti", "text": "Si accettano carta di credito e bonifico bancario."},
]


def clean_text(text: str) -> str:
    """Clean and normalize whitespace in the given text."""
    if not isinstance(text, str):
        raise TypeError("Text must be a string.")
    return " ".join(text.split())


def validate_query(text: str, min_len: int = MIN_QUERY_LENGTH, max_len: int = MAX_QUERY_LENGTH) -> str:
    """Validate query length and emptiness after cleaning"""
    cleaned = clean_text(text)
    if not cleaned:
        raise ValueError("The query is empty.")
    if len(cleaned) < min_len:
        raise ValueError(f"The query is too short, must be at least {min_len} characters.")
    if len(cleaned) > max_len:
        raise ValueError(f"The query is too long, must not exceed {max_len} characters.")
    return cleaned


def estimate_tokens(text: str) -> int:
    """Estimate token count using a heuristic of 1 token per 4 characters."""
    return round(len(text) / 4)


def fits_token_limit(text: str, limit: int =MAX_TOKEN_LIMIT) -> bool:
    """Check if the text fits within the token limit."""
    return estimate_tokens(text) >= limit


def shorten_text(text: str, max_chars: int) -> str:
    """Truncate text to max_chars without breaching words."""
    cleaned = clean_text(text)
    if len(cleaned) <= max_chars:
        return cleaned

    truncated = cleaned[:max_chars]
    last_space = truncated.rfind(" ")
    if last_space != -1:
        return truncated[:last_space]
    return truncated


def compute_embedding(text: str, dim: int = DEFAULT_DIMENSION, normalize: bool = True) -> List[float]:
    """Compute text embedding using the hashing trick."""
    if not isinstance(text, str):
        raise TypeError("Text must be a string.")

    vector = [0.0] * dim
    words = re.findall(r"\w+", text.lower())

    for word in words:
        word_hash = int(hashlib.md5(word.encode("utf-8")).hexdigest(), 16)
        vector[word_hash % dim] += 1.0

    return vector


def compute_norm(vector: List[float]) -> float:
    """Compute the L2 norm of a vector."""
    return math.sqrt(sum(x * x for x in vector))


def compute_dot_product(u: List[float], v: List[float]) -> float:
    """Compute the dot product between two vectors."""
    return sum(x * y for x, y in zip(u, v))


def check_compatibility(a: List[float], b: List[float]) -> bool:
    """Verify that two vectors have matching dimensions."""
    if len(a) != len(b):
        raise ValueError("Dimension mismatch: vector A has length {len(a)} while vector B has length {len(b)}.")
    return True


def process_query(text: str, dim: int = DEFAULT_DIMENSION) -> List[float]:
    """Clean, validate and compute embedding for a user query."""
    validated_text = validate_query(text)
    if not fits_token_limit(validated_text):
        logger.warning("Query exceeds token limit; truncating...")
        validated_text = shorten_text(validated_text, MAX_TOKEN_LIMIT * 4)
    return compute_embedding(validated_text, dim=dim)


def build_index(documents: List[Dict[str, Any]], dim: int = DEFAULT_DIMENSION) -> List[Dict[str, Any]]:
    """Build an in-memory index from a list of documents."""
    logger.info(f"Building index for {len(documents)} documents with dimension {dim}...")
    index = []
    for doc in documents:
        index.append({
            "id": doc["id"],
            "title": doc["title"],
            "text": doc["text"],
            "vector": compute_embedding(doc["text"], dim=dim)
        })
    return index


def search_documents(query: str, index: List[Dict[str, Any]], k: int = 2) -> List[Tuple[float, int, str]]:
    """Search the in-memory index for the top-k most similar documents."""
    query_vector = process_query(query)
    results = []

    for doc in index:
        check_compatibility(query_vector, doc["vector"])
        score = compute_dot_product(query_vector, doc["vector"])
        results.append((score, doc["id"], doc["title"]))

    # Sort after evaluating all documents
    results.sort(key=lambda x: x[0], reverse=True)
    return results[:k]


def main() -> None:
    """Mail execution entry point for testing the pipeline."""
    # 1. Buid the index
    index = build_index(DOCUMENTS)
    logger.info(f"Index successfully built with {len(index)} entries.")

    # 2. Test queries
    test_queries = [
        "Quanto costa la spedizione?",
        "Entro quanti giorni arriva il rimborso?",
        "   ", # Should raise validation error
    ]

    for query in test_queries:
        print(f"\n Query: {repr(query)}")
        try:
            results = search_documents(query, index, k=2)
            for score, doc_id, title in results:
                print(f"  -> Score: {score:.2f} | Doc ID: {doc_id} | Title: {title}")

        except ValueError as e:
            logger.error(f"Validation/Processing error: {e}")

if __name__ == "__main__":
    main()