
"""
Advanced Vector Store Module
------------------------------------
Implements an in-memory vector database with CRUD operations, metadata aggregation, 
vector normalization, dot product, Euclidean distance, and cosine similarity rankings.
"""

import math
import logging
from typing import Dict, List, Tuple, Any, Optional

# Configure structuring logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
)
logger = logging.getLogger(__name__)

# Constants
VECTOR_DIMENSION = 3

# Document corpus
DOCUMENT_RECORDS: List[Dict[str, Any]] = [
    {
        "id": 1,
        "testo": "il gatto dorme sul divano",
        "vettore": [0.92, 0.05, 0.03],
        "meta": {"categoria": "animali", "anno": 2022},
    },
    {
        "id": 2,
        "testo": "il cane corre nel parco",
        "vettore": [0.88, 0.04, 0.08],
        "meta": {"categoria": "animali", "anno": 2023},
    },
    {
        "id": 3,
        "testo": "il pappagallo impara a parlare",
        "vettore": [0.80, 0.02, 0.18],
        "meta": {"categoria": "animali", "anno": 2024},
    },
    {
        "id": 4,
        "testo": "la pasta al pomodoro è pronta",
        "vettore": [0.05, 0.93, 0.02],
        "meta": {"categoria": "cibo", "anno": 2022},
    },
    {
        "id": 5,
        "testo": "la mela è un frutto dolce",
        "vettore": [0.10, 0.88, 0.02],
        "meta": {"categoria": "cibo", "anno": 2023},
    },
    {
        "id": 6,
        "testo": "il pane fresco profuma",
        "vettore": [0.03, 0.90, 0.07],
        "meta": {"categoria": "cibo", "anno": 2024},
    },
    {
        "id": 7,
        "testo": "il computer si avvia piano",
        "vettore": [0.02, 0.03, 0.95],
        "meta": {"categoria": "tecnologia", "anno": 2022},
    },
    {
        "id": 8,
        "testo": "il telefono ha una nuova batteria",
        "vettore": [0.04, 0.06, 0.90],
        "meta": {"categoria": "tecnologia", "anno": 2023},
    },
    {
        "id": 9,
        "testo": "il robot impara dai dati",
        "vettore": [0.30, 0.02, 0.68],
        "meta": {"categoria": "tecnologia", "anno": 2024},
    },
]


def build_vector_database(documents: List[Dict[str, Any]]) -> Dict[int, Dict[str, Any]]:
    """
    Builds an in-memory dictionary database indexing records by their unique ID.

    Args:
        documents: List of raw document dictionaries.

    Returns:
        A dictionary mapping record IDs to record dictionaries.
    """

    database = {}
    for record in documents:
        database[record["id"]] = dict(record)
    return database


# Initialize global database instance
db = build_vector_database(DOCUMENT_RECORDS)


def insert_record(database: Dict[int,  Dict[str, Any]], record_id: int, text: str, vector: List[float], metadata: Dict[str, Any]) -> None:
    """Inserts a new record into the database with duplicate and dimension validation."""
    if record_id in database:
        raise ValueError(f"ID {record_id} già presente nel database.")

    if len(vector) != VECTOR_DIMENSION:
        raise ValueError(f"Dimensione vettoriale errata: {len(vector)} anziché {VECTOR_DIMENSION}.")
    
    database[record_id] = {
        "id": record_id,
        "testo": text,
        "vettore": vector,
        "meta": metadata
    }


def read_record(database: Dict[int, Dict[str, Any]], record_id: int) -> Optional[Dict[str, Any]]:
    """Retrieves a record by its ID, returning None if it does not exist."""
    return database.get(record_id)


def delete_record(database: Dict[int, Dict[str, Any]], record_id: int) -> bool:
    """Deletes a record by ID, returning True if successful or False if not found."""
    if record_id not in database:
        return False
    del database[record_id]
    return True


def update_record(database: Dict[int, Dict[str, Any]], record_id: int, text: Optional[str] = None, vector: Optional[List[float]] = None, meta: Optional[Dict[str, Any]] = None) -> None:
    """Updates specific fields of an existing record with strict validation."""
    if record_id not in database:
        raise ValueError(f"ID {record_id} non trovato non trovato nel database.")
    update_record = dict(database[record_id])

    if text is not None:
        update_record["testo"] = text
    if vector is not None:
        if len(vector) != VECTOR_DIMENSION:
            raise ValueError(f"Dimensione vettoriale errata: {len(vector)} anziché {VECTOR_DIMENSION}.")
        update_record["vettore"] = vector
    if neta is not None:
        update_record["meta"] = meta

    database[record_id] = update_record


def count_by_metadata(database: Dict[int, Dict[str, Any]], field:str) -> Dict[Any, int]:
    """Counts records grouped by a specific metadata field."""
    counts = {}
    for record in database.values():
        val = record["meta"].get(field)
        counts[val] = counts.get(val, 0) + 1
    return counts


def calculate_norm(vector: List[float]) -> float:
    """Calculates the L2 norm (magnituda) of a vector."""
    return math.sqrt(sum(x * x for x in vector))


def normalize_vector(vector: List[float]) -> List[float]:
    """Normalizes a vector to unit length (norm = 1.0), raising ValueError for zero vectors."""
    norm_val = calculate_norm(vector)
    if norm_val == 0.0:
        raise ValueError("Vettore nullo: impossibile normalizzare.")
    return [x / norm_val for x in vector]


def calculate_cosine_similarity(u: List[float], v: List[float]) -> float:
    """
    Calculates the cosine similarity between two numeric vectors.

    Args:
        u: First embedding vector.
        v: Second embedding vector.

    Returns:
        Cosine similarity score as a float between -1.0 and 1.0.
    """
    dot_product = sum(a * b for a, b in zip(u, v))
    norm_u = calculate_norm(u)
    norm_v = calculate_norm(v)

    if norm_u == 0.0 or norm_v == 0.0:
        return 0.0
    
    return dot_product / (norm_u * norm_v)


def calculate_dot_product(u: List[float], v: List[float]) -> float:
    """Calculates the dot product of two vectors."""
    return sum(a * b for a, b in zip(u, v))


def calculate_euclidean_distance(u: List[float], v: List[float]) -> float:
    """Calculates the Euclidean distance between two vectors."""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(u, v)))

def main() -> None:
    """Demonstrates database operations, normalization, and similarity metrics."""

    print("--- 1. Test Operazioni CRUD ---")
    test_db = dict(db)
    insert_record(test_db, 10, "il tablet ha schermo grande", [0.03, 0.04, 0.93], {"categoria": "tecnologia", "anno": 2026})
    print(f"Record totali dopo inserimento: {len(test_db)} (Originale: {len(db)})")

    # Test eccezioni inserimento
    for args in [(10, "doppione", [0.1, 0.1, 0.8], {}), (11, "troppo corto", [0.5, 0.5], {})]:
        try:
            insert_record(test_db, *args)
        except ValueError as e:
            print(f"Intercettata eccezione prevista: {e}")


    print("\n--- 2. Test Lettura e Aggiornamento ---")
    print(f"Testo record 4: {read_record(db, 4)["testo"] if read_record(db, 4) else "Non trovato"}")

    valid_ids = (1, 5, 99)
    texts = [read_record(db, i)["testo"] for i in valid_ids if read_record(db, i) is not None]
    print(f"Testi recuperati in batch: {texts}")

    print("\n--- 3. Test Normalizzazione Vettoriale ---")
    print(f"Norma e normalizzazione di [3, 4]: {calculate_norm([3, 4])}, {normalize_vector([3, 4])}")

    norms_before = [round(calculate_norm(r["vettore"]), 3) for r in db.values()]
    norms_after = [round(calculate_norm(normalize_vector(r["vettore"])), 3) for r in db.values()]
    print(f"Norme prima della normalizzazione: {norms_before[:4], "..."}")
    print(f"Norme dopo la normalizzazione: {norms_after[:4], "..."}")


    print("\n--- 4. Test Metriche di Similarità e Distanza ---")
    query_vector = [0.9, 0.1, 0.0]
    candidates = [
        ("A doppio", [1.8, 0.2, 0.0]),
        ("B metà", [0.45, 0.05, 0.0]),
        ("id 1", db[1]["vettore"])
    ]

    print(f"{'Candidato':<12} | {'Coseno':<8} | {'Dot Product':<12} | {'Distanza Euclidea'}")
    print("-" * 55)
    for name, v in candidates:
        cos = calculate_cosine_similarity(query_vector, v)
        dot = calculate_dot_product(query_vector, v)
        dist = calculate_euclidean_distance(query_vector, v)
        print(f"{name:<12} | {round(cos, 2):<8} | {round(dot, 2):<12} | {round(dist, 2)}")


    print("\n--- 5. Aggregazione Metadati ---")
    cat_counts = count_by_metadata(db, "categoria")
    print(f"Conteggio per categoria: {cat_counts}")
    print(f"Categorie ordinate alfabeticamente: {sorted(cat_counts.keys())}")

if __name__ == "__main__":
    main()