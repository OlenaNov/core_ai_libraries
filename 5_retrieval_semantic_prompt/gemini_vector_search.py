
import logging
import os
import math
from typing import Any, Dict, List, Tuple, Optional
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("GeminiVectorSearch")

# Constants
DEFAULT_MODEL = "gemini-embedding-001"  
DEFAULT_DIMENSION = 3072             
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
        raise TypeError(f"Text must be a string.")
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
    """Estimate token count using s heuristic of 1 token per 4 characters."""
    return math.ceil(len(text) / 4)


def fits_token_limit(text: str, limit: int = MAX_TOKEN_LIMIT) -> bool:
    """Check if the text fits within the token limit."""
    return estimate_tokens(text) <= limit


def shorten_text(text: str, max_chars: int) -> str:
    """Truncate text to max_chars without breaking words."""
    cleaned = clean_text(text)
    if len(cleaned) <= max_chars:
        return cleaned
    truncated = cleaned[:max_chars]
    last_space = cleaned.rfind(" ")

    if last_space != -1:
        return truncated[:last_space]
    return truncated


def compute_dot_product(u: List[float], v: List[float]) -> float:
    """Compute dot product between two vectors."""
    return sum(x * y for x, y in zip(u, v))


def check_compatibility(a: List[float], b: List[float])-> bool:
    """Verify that two vectors have matching dimensions."""
    if len(a) != len(b):
        raise ValueError(f"Dimension mismatch: vector A has length {len(a)} while vector B has length {len(b)}.")
    return True


class GeminiVectorSearchEngine:
    """In-memory vector search engine powered by the Google GenAI SDK."""
    def __init__(self, model_name: str = DEFAULT_MODEL) -> None:
        """Initialize the Gemini client and model configuration."""
        if "GEMINI_API_KEY" not in os.environ:
            logger.warning("GEMINI_API_KEY environment variable not explicitly found in os.environ. Relying on default client auth.")

        self.client = genai.Client()
        self.model_name = model_name
        logger.info(f"Initialized GeminiVectorSearchEngine witn model: {self.model_name}")

    def get_embedding(self, text: str, task_type: str = "RETRIEVAL_QUERY") -> List[float]:
        """Call the Gemini API to generate content embeddings."""
        config = types.EmbedContentConfig(task_type=task_type)

        response = self.client.models.embed_content(
            model=self.model_name,
            contents=text,
            config=config,
        )

        return response.embeddings[0].values

    def build_index(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Build an in-memory vector index calling Gemini API for each document."""
        logger.info(f"Building index for {len(documents)} documents using model {self.model_name}...")
        index = []

        for doc in documents:
            vector = self.get_embedding(doc["text"], task_type="RETRIEVAL_DOCUMENT")
            index.append({
                "id": doc["id"],
                "title": doc["title"],
                "text": doc["text"],
                "vector": vector,
            })
        logger.info("Index successfully built with Gemini embeddings.")
        return index

    def search(self, query: str, index: List[Dict[str, Any]], k: int = 2) -> List[Tuple[float, int, str]]:
        """Search the in memory index using a query embedding."""
        validated_query = validate_query(query)
        if not fits_token_limit(validated_query):
            logger.warning("Query exceeds token limit, truncating...")
            validated_query = shorten_text(validated_query, MAX_TOKEN_LIMIT * 4)

        # Genera il vettore per la query usando il task_type di ricerca
        query_vector = self.get_embedding(validated_query, task_type="RETRIEVAL_QUERY")

        results = []
        for doc in index:
            check_compatibility(query_vector, doc["vector"])
            score = compute_dot_product(query_vector, doc["vector"])
            results.append((score, doc["id"], doc["title"]))

        results.sort(key=lambda x: x[0], reverse=True)
        return results[:k]



def main() -> None:
    """Main execution entry point demonstrating the Gemini API integration."""
    try:
        # Istanzione del motore di ricerca
        engine = GeminiVectorSearchEngine(model_name=DEFAULT_MODEL)

        # 1. Costruzione dell'indice 
        index = engine.build_index(DOCUMENTS)

        # 2. Eseguizione del test di ricerca semantica
        queries = [
            "Quanto costa la spedizione?",
            "Entro quanti giorni arriva il rimborso?",
        ]
        for q in queries:
            print(f"\nQuery: {repr(q)}")
            results = engine.search(q, index, k=2)
            for score, doc_id, title in results:
                print(f"  -> Score: {score:.4f} | Doc ID: {doc_id} | Title: {title}")
                      
    except Exception as e:
        logger.error(f"An error occurred during Gemini API execution: {e}")

if __name__ == "__main__":
    main()

