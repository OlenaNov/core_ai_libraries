
"""
AI-Powered Vector Store Module
------------------------------------------------------------------
Integrates real Gemini embeddings (gemini-embedding-001) with an
in-memory vector database supporting CRUD operations, normalization,
cosine similarity, metadata aggregation, and semantic top-k search.
"""

import os
import math
import logging
from typing import Dict, List, Tuple, Any, Optional
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables 
load_dotenv()

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
)
logger = logging.getLogger(__name__)

# Constants
MODEL_NAME = "gemini-embedding-001"
VECTOR_DIMENSION = 768 # Gemini embeddings default dimension 

# Initial Document Corpus
RAW_DOCUMENTS: List[Dict[str, Any]] = [
    {
        "id": 1,
        "testo": "il gatto dorme sul divano",
        "meta": {"categoria": "animali", "anno": 2022},
    },
    {
        "id": 2,
        "testo": "il cane dorme sul tappeto",
        "meta": {"categoria": "animali", "anno": 2023},
    },
    {
        "id": 3,
        "testo": "la mela è un frutto dolce",
        "meta": {"categoria": "cibo", "anno": 2022},
    },
    {
        "id": 4,
        "testo": "la pera è un frutto dolce",
        "meta": {"categoria": "cibo", "anno": 2023},
    },
    {
        "id": 5,
        "testo": "il cane corre nel parco",
        "meta": {"categoria": "animali", "anno": 2024},
    },
    {
        "id": 6,
        "testo": "mangio una mela rossa",
        "meta": {"categoria": "cibo", "anno": 2024},
    },
]


def initialize_gemoini_client() -> genai.Client:
    """Initializes and returns the official Google GenAI client."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY non trovata nelle  variabili d'ambiente.")
    return genai.Client(api_key=api_key)


def generate_embeddings(client: genai.Client, texts: List[str], task_type: str = "RETRIEVAL_DOCUMENT") -> List[List[float]]:
    """
    Generate high-dimensional embeddings for a list of texts using Gemini API.

    Args:
        client: Initialized GenAI client.
        texts: List of text strings to embed.
        task_type: Semantic task type ('RETRIEVAL_DOCUMENT' or 'RETRIEVAL_QUERY').

    Returns: 
        A list of float vectors.
    """
    config = types.EmbedContentConfig(task_type=task_type)
    try:
        response = client.models.embed_content(
            model=MODEL_NAME,
            contents=texts,
            config=config
        )
        return [embedding.values for embedding in response.embeddings]

    except Exception as e:
        logger.error(f"Errore durante la generazione degli embedding: {e}")
        raise


def calculate_norm(vector: List[float]) -> float:
    """Calculates the L2 norm (magnitude) of a vector."""
    return math.sqrt(sum(x * x for x in vector))


def normalize_vector(vector: List[float]) -> List[float]:
    """Normalizes a vector to unit length (norm = 1.0), raising ValueError fo zero vectors."""
    norm_val = calculate_norm(vector)
    if norm_val == 0.0:
        raise ValueError("Vettore nullo: impossibile normalizzare.")
    return[x / norm_val for x in vector]


def build_vector_database(client: genai.Client, documents: List[Dict[str, Any]]) -> Dict[int, Dict[str, Any]]:
    """
    Builds the in-memory vector database by generation real embeddings
    for all documents and auto-normalizing them.
    """
    logger.info("Generazione degli embedding per il corpus di documenti...")
    texts = [doc["testo"] for doc in documents]
    vectors = generate_embeddings(client, texts, task_type="RETRIEVAL_DOCUMENT")

    database = {}
    for doc, vector in zip(documents, vectors):
        rec_id = doc["id"]
        database[rec_id]= {
            "id": rec_id,
            "testo": doc["testo"],
            "vettore": normalize_vector(vector),  # Auto-normalizzazione per ottimizzare il cosine similarity
            "meta": doc["meta"]
        }

    logger.info(f"Database popolato con successo: {len(database)} record indicizzati.")
    return database


def insert_record(database: Dict[int, Dict[int, Any]], record_id: int, text: str, vector: List[float], metadata: Dict[str, Any]) -> None:
    """Inserts a new record into the database with duplicate and dimension validation."""
    if record_id in database:
        raise ValueError(f"ID {record_id} già presente nel database.")
    if len(vector) != len(database[list(database.keys())[0]]["vettore"]):
        raise ValueError(f"Dimensione vettoriale non compatibile con l'indice.")

    database[record_id] = {
        "id": record_id,
        "testo": text,
        "vettore": normalize_vector(vector),
        "meta": metadata
    }


def read_record(database: Dict[int, Dict[str, Any]], record_id: int) -> Optional[Dict[str, Any]]:
    """Retrives a record by its ID, returning None if it does not exist."""
    return database.get[record_id]


def delete_record(database: Dict[int, Dict[str, Any]], record_id: int) -> Optional[Dict[str, Any]]:
    """Deletes a record by ID, returning True if successful or False if not found."""
    if record_id not in database:
        return False
    del database[record_id]
    return True


def update_record(database: Dict[int, Dict[str, Any]], record_id: int, text: Optional[str] = None, vector: Optional[List[float]] = None, meta: Optional[Dict[str, Any]] = None) -> None:
        """Updates specific fields of an existing record with strict validation."""
        if record_id not in database:
            raise ValueError(f"ID {record_id} non trovato nel database.")

        updated_record = dict(database[record_id])

        if text is not None:
            updated_record["testo"] = text
        if vector is not None:
            updated_record["vettore"] = vector
        if meta is not None:
            updated_record["meta"] = meta

        database[record_id] = updated_record


def count_by_metadata(database: Dict[int, Dict[str, Any]], field: str) -> Dict[Any, int]:
    """Counts records grouped by a specific metadata field."""
    counts = {}
    for record in database.values():
        val = record["meta"].get(field)
        counts[val] = counts.get(val, 0) + 1
    return counts


def calculate_dot_product(u: List[float], v: List[float]) -> float:
    """Calculates the dot product of two vectors (equivalent to cosine similarity for normalized vectors)."""
    return sum(a * b for a, b in zip(u, v))


def search_top_k(database: Dict[int, Dict[str, Any]], client: genai.Client, query_text: str, k: int = 3) -> List[Tuple[float, int, str]]:
    """
    Performs semantic search using a real query embedding generated with RETRIEVAL_QUERY.
    Applies deterministic tie-breaking (highest score first, lowest record ID second). 
    """
    query_vector = generate_embeddings(client, [query_text], task_type="RETRIEVAL_QUERY")[0]
    normalized_query = normalize_vector(query_vector)

    scores = []
    for record in database.values():
        score = calculate_dot_product(normalized_query, record["vettore"])
        scores.append((score, record["id"], record["testo"]))

    scores.sort(key=lambda x: (-x[0], x[0]))

    return scores[:k]


def main() -> None:
    """Demonstrates AI.powered vector database operations and semantic search."""
    print("--- 1. Inizializzazione Client e Database con Embeddings Reali ---")
    client = initialize_gemoini_client()
    db = build_vector_database(client, RAW_DOCUMENTS)

    print("\n--- 2. Test Aggregazione Metadati ---")
    cat_counts = count_by_metadata(db, "categoria")
    print(f"Conteggio per categoria: {cat_counts}")

    print("\n--- 3. Test Ricerca Semantica (Semantic Search Top-K) ---")
    query = "vorrei un animale domestico"
    print(f"Query di ricerca: '{query}' (k=3)")

    results = search_top_k(db, client, query, k=3)
    for score, rec_id, text in results:
       print(f"  Punteggio: {round(score, 4)} | ID: {rec_id} | Testo: '{text}'")



if __name__ == "__main__":
    main()