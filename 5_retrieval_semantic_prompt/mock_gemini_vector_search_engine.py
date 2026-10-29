
import hashlib
import logging
import math
import re
from types import SimpleNamespace
from typing import Any, Dict, List, Optional, Tuple, Union

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("GeminiVectorSearchEngine")

# Constants
DEFAULT_DIMENSION = 3072
MIN_QUERY_LENGTH = 3
MAX_QUERY_LENGTH = 500
MAX_TOKEN_LIMIT = 512

ROLE_MAPPING = {
    "query": "RETRIEVAL_QUERY",
    "document": "RETRIEVAL_DOCUMENT",
    "question": "QUESTION_ANSWERING"
}

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
    """Validate query length and emptiness after cleaning."""
    cleaned = clean_text(text)

    if not cleaned:
        raise ValueError("The query is empty.")
    if len(cleaned) < min_len:
        raise ValueError("The query is too short, must be at least {min_len} characters.")
    if len(cleaned) > max_len:
        raise ValueError("The query is too long, must be not exceed {max_len} characters.")
    return cleaned


def estimate_tokens(text: str) -> int:
    """Estimate token count using a heuristic of 1 token per 4 characters."""
    return round(len(text) / 4)


def fits_token_limit(text: str, limit: int = MAX_TOKEN_LIMIT) -> bool:
    """Check if the text within the token limit."""
    return estimate_tokens(text) <= limit


def shorten_text(text: str, max_chars: int) -> str:
    """Truncate text to max_chars without breaking words."""
    cleaned = clean_text(text)
    if len(cleaned) <= max_chars:
        return cleaned
    truncated = cleaned[:max_chars]
    last_space = truncated.rfind(" ")
    if last_space != -1:
        return truncated[:last_space]
    return truncated


def _compute_mock_embedding(text: str, dim: int = DEFAULT_DIMENSION, normalize: bool = True) -> List[float]:
    """Produce a simulated embedding vector using the hashing trick, stripping prompt prefixes."""
    # Robustly strip any model or task instruction prefixes (e.g., task:,  title:, query:, document:, with o without pipe)
    cleaned_text = re.sub(
        r"^(?:task|title|query|document):[^|]*?(?:\|\s*(?:query|text):\s*|$)",
        "",
        text,
        flags=re.IGNORECASE,
    )
    # Fallback to strip standalone prefix headers if any remain
    cleaned_text = re.sub(r"^(?:query|document|text):\s*", "", cleaned_text, flags=re.IGNORECASE)

    vector = [0.0] * dim
    words = re.findall(r"\w+", cleaned_text.lower())

    for word in words:
        word_hash = int(hashlib.md5(word.encode("utf-8")).hexdigest(), 16)
        vector[word_hash % dim] += 1

    norm = math.sqrt(sum(x * x for x in vector))
    if normalize and norm > 0:
        vector = [x / norm for x in vector]

    return vector


class MockGeminiEmbeddingClient:
    """Simulated Google GenAI Embedding Client for offline experimentation."""
    
    def embed_content(
    self,
    model: str,
    contents: Union[str, List[str]],
    config: Optional[Any] = None,
) -> SimpleNamespace:
        """Simulated embed_content API call matching Google GenAI SDK behavior."""
        if model not in ("gemini-embedding-001", "gemini-embedding-2"):
            raise ValueError(f"Unknown on unsupported model: {model}")

        dim = getattr(config, "output_dimensionality", None) or DEFAULT_DIMENSION
        texts = [contents] if isinstance(contents, str) else list(contents)

        # gemini-embedding-2 aggregates multiple texts if passed together
        if model == "gemini-embedding-2" and len(texts) > 1:
            texts = [" ".join(texts)]

        normalize = not (model == "gemini-embedding-001" and dim != DEFAULT_DIMENSION)
        vectors = [_compute_mock_embedding(t, dim, normalize) for t in texts]

        return SimpleNamespace(embeddings=[SimpleNamespace(values=v) for v in vectors])


# Initialize mock client and types namespace mimicking google.genai
client = SimpleNamespace(models=MockGeminiEmbeddingClient())
types = SimpleNamespace(EmbedContentConfig=lambda **kw: SimpleNamespace(**kw))


def prepare_query_prompt(query: str, task_type: str = "search result") -> str:
    """Format query prompt with tasks introductions for Gemini-embedding-2."""
    return f"task: {task_type} | query: {query}"


def prepare_document_prompt(content: str, title: Optional[str] = None) -> str:
    """Format document text with title prefix for embedding."""
    doc_title = title or "none"
    return f"title: {doc_title} | text: {content}"


def get_embedding_config(role: str) -> Any:
    """Return appropriate EmbedContentConfig with task_type for gemini-embedding-001."""
    if role not in ROLE_MAPPING:
        raise ValueError(f"Invalid role '{role}'. Valid roles are {list(ROLE_MAPPING.keys())}")
    return types.EmbedContentConfig(task_type=ROLE_MAPPING[role])


def prepare_request(text: str, model: str, role: str = "query", title: Optional[str] = None) -> Tuple[str, Optional[Any]]:
    """Prepare text and configuration based on the chosen Gemini embedding model version."""
    if model == "gemini-embedding-2":
        formatted_text = (
            f"query: {text}" if role == "query" else f"document: {text}"
            )
        return formatted_text, None
    elif model == "gemini-embedding-001":
        if role == "document":
            formatted_text = prepare_document_prompt(text, title)
        else:
            formatted_text = text
        return formatted_text, get_embedding_config(role)
    
    raise ValueError(f"Unknown model identifier: {model}")


def compute_dot_product(u: List[float], v: List[float]) -> float:
    """Compute dot product between two embedding vectors."""
    return sum(x * y for x, y in zip(u, v))


def check_compatibility(a: List[float], b: List[float]) -> bool:
    """Verify that two vectors have matching dimensions."""
    if len(a) != len(b):
        raise ValueError(f"Dimension mismatch: vector A has length {len(a)} while vector B has length {len(b)}.")
    return True


def build_vector_index(documents: List[Dict[str, Any]], model: str = "gemini-embedding-2", dim: int = DEFAULT_DIMENSION) -> List[Dict[str, Any]]:
    """Build an in-memory vector index using the specified Gemini model client."""
    logger.info(f"Building index for {len(documents)} documents using model {model} (dim={dim})...")
    index = []

    for doc in documents:
        prep_text, config = prepare_request(doc["text"], model=model, role="document", title=doc["title"])
        response = client.models.embed_content(model=model, contents=prep_text, config=config)
        vector = response.embeddings[0].values

        index.append({
            "id": doc["id"],
            "title": doc["title"],
            "text": doc["text"],
            "vector": vector
        })
    return index


def search_vector_index(query: str, index: List[Dict[str, Any]], model: str = "gemini-embedding-2", k: int = 2) -> List[Tuple[float, int, str]]:
    """Search the in-memory index for top-k similar documents given a user query."""
    validated_query = validate_query(query)
    if not fits_token_limit(validated_query):
        logger.warning("Query exceeds token limit: trunking...")
        validated_query = shorten_text(validated_query, MAX_TOKEN_LIMIT * 4)

    prep_query, config = prepare_request(validated_query, model=model, role="query")
    response = client.models.embed_content(model=model, contents=prep_query, config=config)
    query_vector = response.embeddings[0].values

    results = []
    for doc in index:
        check_compatibility(query_vector, doc["vector"])
        score = compute_dot_product(query_vector, doc["vector"])
        results.append((score, doc["id"], doc["title"]))

    results.sort(key=lambda x: x[0], reverse=True)
    return results[:k]



def main() -> None:
    """Main execution entry point demonstrating multi-model index building and retrieval."""
    # Test with gemini-embedding-2
    print("--- Testing with gemini-embedding-2 ---")
    index_v2 = build_vector_index(DOCUMENTS, model="gemini-embedding-2")

    queries = [
        "Quanto costa la spedizione?",
        "Entro quanti giorni arriva il rimborso?",
    ]

    for q in queries:
        print(f"\nQuery: {repr(q)}")
        results = search_vector_index(q, index_v2, model="gemini-embedding-2", k=2)
        for score, doc_id, title in results:
            print(f"  -> Score: {score:.2f} | Doc ID: {doc_id} | Title: {title}")

    # Test with gemini-embedding-001
    print("\n--- Testing with gemini-embedding-001 ---")
    config_001 = types.EmbedContentConfig(output_dimensionality=512)
    index_001 = build_vector_index(DOCUMENTS, model="gemini-embedding-001", dim=512)

    for q in queries:
        print(f"\nQuery: {repr(q)}")
        results = search_vector_index(q, index_001, model="gemini-embedding-001", k=2)
        for score, doc_id, title in results:
            print(f"  -> Score: {score:.2f} | Doc ID: {doc_id} | Title: {title}")


if __name__ == "__main__":
    main()