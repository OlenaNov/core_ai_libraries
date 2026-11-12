
"""
Production-Grade RAG Pipeline Powered by Google Gemini AI.
"""

import logging
import math
import os
from typing import Any, Dict, List, Optional, Tuple
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ServerError


# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logger = logging.getLogger("GeminiRAGSystem")

# Load environment variables
load_dotenv()

# Initialize Gemini Client
client = genai.Client()

# Configuration Constants
MODEL_TEXT = "gemini-3.5-flash"
MODEL_EMBEDDING = "gemini-embedding-2"
DIMENSION = 768

# ==========================================
# 1. EMBEDDING & UTILITIES ENGINE
# ==========================================

def compute_embedding(text: str, dim: int = DIMENSION) -> List[float]:
    """
    Compute a numerical embedding vector for a given text using Gemini API.

    Args:
        text (str): Input text string.
        dim (int): Output vector dimensionality.

    Returns:
        List[float]: Embedding vector values.
    """
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Input text must be a non-empty string.")

    try:
        response = client.models.embed_content(
            model=MODEL_EMBEDDING,
            contents=text,
            config=types.EmbedContentConfig(output_dimensionality=dim),
        )
        return response.embeddings[0].values
    except Exception as e:
        logger.error(f"Failed to generate embedding: {e}")
        raise


def compute_document_embedding(title: str, text: str, dim: int = DIMENSION) -> List[float]:
    """Compute embedding for document chunks using title-text semantic formatting."""
    formatted_content = f"title: {title} | text: {text}"
    return compute_embedding(formatted_content, dim=dim)


def compute_query_embedding(query: str, dim: int = DIMENSION) -> List[float]:
    """Compute embedding for user queries optimized for retrieval tasks."""
    cleaned_query = " ".join(query.split())
    if not cleaned_query:
        raise ValueError("Query cannot be empty or contain only whitespace.")
    
    formatted_query = f"task: question-answering | query: {cleaned_query}"
    return compute_embedding(formatted_query, dim=dim)


def check_vector_compatibility(vector_a: List[float], vector_b: List[float]) -> bool:
    """Validate that two embedding vectors share identical dimensionality."""
    if len(vector_a) != len(vector_b):
        raise ValueError(f"Vector dimensionality mismatch: {len(vector_a)} vs {len(vector_b)}")
    return True


def estimate_tokens(text:str) -> int:
    """Estimate token count using standard ~4 characters per token heuristic."""
    return math.ceil(len(text) / 4)


# ==========================================
# 2. OFFLINE INDEXING PIPELINE
# ==========================================

def build_vector_index(chunks: List[Dict[str, Any]], dim: int = DIMENSION) -> List[Dict[str, Any]]:
    """Build vector index by calculating embeddings for all document chunks."""
    index = []
    for chunk in chunks:
        vector = compute_document_embedding(chunk["source"], chunk["text"], dim=dim)
        index.append({**chunk, "vector": vector})

    logger.info(f"Vector index successfully built with {len(index)} items.")
    return index


def add_chunk_to_index(
        index: List[Dict[str, Any]],
        source: str,
        text: str,
        dim: int = DIMENSION
) -> int:
    """Dynamically add a new chunk and its embedding to the existing index."""
    if not source or not text:
        raise ValueError("Source and text cannot be empty.")

    new_id = len(index)
    vector = compute_document_embedding(source, text, dim=dim)

    new_chunk = {
        "id": new_id,
        "source": source,
        "text": text,
        "vector": vector
    }
    index.append(new_chunk)
    logger.info(f"Added new chunk ID {new_id} from source '{source}' to index.")
    return new_id


# ==========================================
# 3. ONLINE QUERY & RETRIEVAL PIPELINE
# ==========================================

def search_similar_chunks(query: str, index: List[Dict[str, Any]], k: int = 2) -> List[Tuple[float, Dict[str, Any]]]:
    """Retrieve top-k similar chunks using dot product over normalized vectors."""
    query_vector = compute_query_embedding(query)
    results = []

    for item in index:
        check_vector_compatibility(query_vector, item["vector"])
        score = sum(q * d for q, d in zip(query_vector, item["vector"]))      
        results.append((score, item))

    results.sort(key=lambda x: x[0], reverse=True)
    return results[:k]


def retrieve_with_threshold(query: str, index: List[Dict[str, Any]], k: int = 2, threshold: float = 0.2) -> List[Tuple[float, Dict[str, Any]]]:
    """Retrieve top-k similar chunks filtering out those bellow the similarity threshold."""
    results = search_similar_chunks(query, index, k=k)
    filtered = [r for r in results if r[0] >= threshold]
    return filtered


def fit_within_budget(retrieved_results: List[Tuple[float, Dict[str, Any]]], max_tokens: int) -> Tuple[List[Tuple[float, Dict[str, Any]]], int]:
    """Filter retrieved chunks to fit within the Gemini model token budget."""
    selected = []
    tokens_used = 0

    for score, chunk in retrieved_results:
        cost = estimate_tokens(chunk["text"])
        if tokens_used + cost > max_tokens:
            logger.warning("Token budget exceeded. Truncating context.")
            break
        selected.append((score, chunk))
        tokens_used += cost

    return selected, tokens_used


def build_context_string(retrieved_results: List[Tuple[float, Dict[str, Any]]]) -> str:
    """Format retrieved results into a structured numbered context block."""
    if not retrieved_results:
        return "(Nessun documento trovato)"

    lines = []
    for number, (score, chunk) in enumerate(retrieved_results):
        lines.append(f"[{number}] {chunk['text']} (source: {chunk['source']})")

    return "\n".join(lines)


def build_prompt(query: str, context: str) -> str:
    """Compose final prompt with instructions, retrieved context, and query."""
    return (
        "Rispondi usando solo il contesto fornito. Se l'informazione non è presente, rispondi \"Non lo so\".\n\n"
        f"Contesto:\n{context}\n\n"
        f"Domanda:\n{query}"
    )


def generate_answer(prompt: str) -> str:
    """Send prompt to gemini AI model and return generated response text with error handling."""
    try: 
        response = client.models.generate_content(
            model=MODEL_TEXT,
            contents=prompt
        )
        return response.text
    
    except ServerError as e:
        logger.error(f"Gemini server error: {e}")
        return "[Errore temporaneo del server: il modello è sovraccarico. Riprova tra poco.]"
    except Exception as e:
        logger.error(f"Generation error: {e}")
        raise


# ==========================================
# 4. GEMINI RAG ORCHESTRATOR
# ==========================================

class GeminiRAGPipeline:
    """High-level orchestration class managing offline indexing and on-line Gemini RAG querying."""

    def __init__(self, raw_chunks: List[Dict[str, Any]], dim: int = DIMENSION) -> None:
        self.dim = dim
        logger.info("Initializing Gemini RAG Pipeline...")
        self.index = build_vector_index(raw_chunks, dim=self.dim)
        logger.info("Gemini RAG Pipeline initialized successfully.")

    def query(self, user_query: str, k: int = 2, threshold: float = 0.2, max_tokens: int = 500) -> str:
        """<execute compete end-to-end RAG query flow."""
        logger.info(f"Processing query: '{user_query}'")

        # Retrieval with threshold filtering
        retrieved = retrieve_with_threshold(user_query, self.index, k=k, threshold=threshold)

        # Token budget enforcement 
        budget_results, _ = fit_within_budget(retrieved, max_tokens=max_tokens)

        # Context and prompt construction
        context = build_context_string(budget_results)
        prompt = build_prompt(user_query, context)

        # Generation answer
        answer = generate_answer(prompt)
        return answer


# ==========================================
# EXECUTION DEMO
# ==========================================

if __name__ == "__main__":
    CHUNKS = [
        {"id": 0, "source": "resi.txt", "text": "Il reso è gratuito entro quattordici giorni dalla consegna."},
        {"id": 1, "source": "rimborsi.txt", "text": "Il rimborso arriva entro sette giorni dal ricevimento del reso."},
        {"id": 2, "source": "spedizioni.txt", "text": "La spedizione costa cinque euro e la consegna avviene in tre giorni."},
        {"id": 3, "source": "pagamenti.txt", "text": "Si accettano carta di credito e bonifico bancario."},
    ]

    # Initialize 
    rag_app = GeminiRAGPipeline(CHUNKS)

    # Test Query
    question = "Entro quanti giorni arriva il rimborso?"
    final_answer = rag_app.query(question, k=2, threshold=0.1)

    print("\n--- RISULTATO GEMINI RAG ---")
    print(f"Domanda: {question}")
    print(f"Risposta: {final_answer}")