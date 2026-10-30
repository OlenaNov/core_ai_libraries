
"""
Production-Grade RAG (Retrieval-Augmented Generation) Pipeline.
"""

import hashlib
import logging
import math
import re
from typing import Any, Dict, List, Optional, Tuple
import uuid


# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logger = logging.getLogger("RAGSystem")

# ==========================================
# 1. EMBEDDING & UTILITIES ENGINE
# ==========================================

def compute_text_embedding(text: str, dim: int = 1024) -> List[float]:
    """
    Compute a normalized numerical embedding vector for a given text
    using MD5 hashing over extracted word tokens.

    Args:
        text (str): Input text string embed. 
        dim (int): Vector dimensionality (default: 1024).

    Returns: 
        list[float]: L2-normalized embedding vector.
    """
    if not isinstance(text, str):
        raise TypeError("Input text must be a string.")

    vector = [0.0] * dim
    tokens = re.findall(r"\w+", text.lower())

    for token in tokens:
        # Generate hash index
        token_hash = hashlib.md5(token.encode("utf-8")).hexdigest()
        position = int(token_hash, 16) % dim
        vector[position] += 1.0
        
    # L2 Normalization
    norm = math.sqrt(sum(val * val for val in vector))

    if norm > 0:
        return [val / norm for val in vector]
    return vector


def compute_query_embedding(query: str, dim: int = 1024) -> List[float]:
    """
    Clean, validate and compute embedding vector for a user query.

    Args: 
        query (str): The raw user query.
        dim (int): Target vector dimension. 

    Returns:
        List[float]: Normalized query embedding vector.
    """
    if not isinstance(query, str):
        raise TypeError("Query must be a string.")

    cleaned_query = " ".join(query.split())
    if not cleaned_query:
        raise ValueError("Query cannot be empty or contain only whitespace.")

    return compute_text_embedding(cleaned_query, dim=dim)


def check_vector_compatibility(vector_a: List[float], vector_b: List[float]) -> bool:
    """
    Validate that two embedding vectors share identical dimensionality.

    Raises:
        ValueError: If vector dimensions mismatch.
    """
    if len(vector_a) != len(vector_b):
        raise ValueError(f"Vector dimension mismatch: {len(vector_a)} vs {len(vector_b)}.")
    
    return True


def estimate_tokens(text: str) -> int:
    """Estimate token count based on character length heuristic (~4 chars/token)."""
    return math.ceil(len(text) / 4)


# ==========================================
# 2. OFFLINE INDEXING PIPELINE
# ==========================================

def chunk_documents(documents: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """
    Split raw documents into sentence-level chunks with incremental IDs.

    Args:
        documents (List[Dict[str, str]]): List of raw documents (source, text).

    Returns: 
        List[Dict[str, Any]]: List of structured chunks.
    """
    if not documents:
        raise ValueError("Document list cannot be empty.")

    chunks = []
    for doc in documents:
        if "text" not in doc or "source" not in doc:
            raise KeyError("Each document must contain 'source' and 'text' keys.")

        sentences = doc["text"].split(".")
        for sentence in sentences:
            cleaned_sentence = sentence.strip()
            if cleaned_sentence:
                content_identifier = f"{doc['source']}:{cleaned_sentence}"
                chunk_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, content_identifier))
                
                chunks.append({
                    "id": chunk_id,
                    "source": doc["source"],
                    "text": cleaned_sentence + "."
                })
    logger.info(f"Successfully generated {len(chunks)} chunks from {len(documents)} documents.")
    return chunks


def build_vector_index(chunks: List[Dict[str, Any]], dim: int = 1024) -> List[Dict[str, Any]]:
    """
    Build the vector index by computer embeddings for all document chunks.
    """
    index = []
    for chunk in chunks:
        vector = compute_text_embedding(chunk["text"], dim=dim)
        index.append({**chunk, "vector": vector})

    logger.info(f"Vector index built successfully with {len(index)} items.")
    return index


def add_chunk_to_index(index: List[Dict[str, Any]], source: str, text: str, dim: int = 1024) -> int:
    """
    Dynamically add a new chunk and its embedding to the existing index.
    """
    if not source or not text:
        raise ValueError("Source and text cannot be empty when adding a chunk.")

    new_id = len(index)
    vector = compute_text_embedding(text, dim=dim)

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
    """
    Retrieve the top-k most popular chunks using cosine similarity (dot product on normalized vectors).
    """
    query_vector = compute_query_embedding(query)
    results = []

    for item in index:
        check_vector_compatibility(query_vector, item["vector"])
        score = (sum(q * d for q, d in zip(query_vector, item["vector"])))
        results.append((score, item))

    results.sort(key=lambda x: x[0], reverse=True)
    return results[:k]


def fit_within_budget(retrieved_results: List[Tuple[float, Dict[str, Any]]], max_tokens: int) -> Tuple[List[Tuple[float, Dict[str, Any]]], int]:
    """
    Filter retrieved chunks to fit within the LLM context token budget.
    """

    selected =[]
    tokens_used = 0

    for score, chunk in retrieved_results:
        cost = estimate_tokens(chunk["text"])
        if tokens_used + cost > max_tokens:
            logger.warning(f"Token budget exceeded ({tokens_used + cost}/{max_tokens}). Truncating retrieval.")
            break
        selected.append((score, chunk))
        tokens_used += cost

    return selected, tokens_used


def build_context_string(retrieved_results: List[Tuple[float, Dict[str, Any]]]) -> str:
    """Format retrieved chunks into a structured context block for the prompt."""
    if not retrieved_results:
        return "Nessun documento trovato."

    lines = []
    for rank, (score, chunk) in enumerate(retrieved_results, start=1):
        lines.append(f"[{rank}] {chunk["text"]} (source: {chunk["source"]})")

    return "\n".join(lines)


def build_prompt(query: str, context: str) -> str:
    """Compose the final prompt containing system instructions, context and query."""
    return (
        "Rispondi usando solo il contesto. Se l'informazione non c'è, rispondi \"Non lo so\".\n\n"
        f"Contesto:\n{context}\n\n"
        f"Domanda: {query}"
    )


def mock_llm_generator(prompt: str) -> str:
    """
    Simulate a generative LLM responding strictly base on retrieved context lines.
    """
    lines = [line for line in prompt.splitlines() if line.startswith("[")]
    if not lines:
        return "Non lo so."

    # Extract text from the top ranked context line
    text = lines[0].split("] ", 1)[1].split(" (source", 1)[0]
    return f"Secondo i documenti: {text}"


# ==========================================
# 4. RAG SYSTEM ORCHESTRATOR
# ==========================================

class RAGPipeline:
    """High-level orchestration class managing both Indexing and Queries phases."""

    def __init__(self, raw_documents: List[Dict[str, str]], embedding_dim: int = 1024) -> None:
        self.embedding_dim = embedding_dim
        logger.info("Initializing RAG Pipeline...")

        # Phase 1: Indexing (Offline)
        chunks = chunk_documents(raw_documents)
        self.index = build_vector_index(chunks, dim=self.embedding_dim)
        logger.info(f"Indexing completed. Total indexed chunks: {len(self.index)}")

    def query(self, user_query: str, top_k: int = 2, max_tokens: int = 200) -> str:
        """
        Execute the full online query pipeline:
        Retrieval -> Budget Check -> Context Construction -> Prompt Assembly -> Generation.
        """
        logger.info(f"Processing query: '{user_query}'")

        # Step 1 & 2: Retrieve similar chunks
        raw_results = search_similar_chunks(user_query, self.index, k=top_k)

        # Step 3: Enforce token budget limits
        budget_results, _ = fit_within_budget(raw_results, max_tokens=max_tokens)

        # Step 4: Build context & prompt
        context = build_context_string(budget_results)
        prompt = build_prompt(user_query, context)

        # Step 5: Generate response
        response = mock_llm_generator(prompt)
        return response


# ==========================================
# EXECUTION DEMO
# ==========================================

def main() -> None:
    # Knowledge Base
    kb_documents = [
        {"source": "resi.txt", "text": "Il reso è gratuito entro quattordici giorni dalla consegna. Il prodotto deve essere integro."},
        {"source": "rimborsi.txt", "text": "Il rimborso arriva entro sette giorni dal ricevimento del reso. Il rimborso usa lo stesso metodo di pagamento."},
        {"source": "spedizioni.txt", "text": "La spedizione costa cinque euro. La consegna avviene in tre giorni lavorativi."},
        {"source": "pagamenti.txt", "text": "Si accetta carta di credito e bonifico bancario."},
    ]

    # Initialize RAG System
    rag = RAGPipeline(kb_documents)

    # Test Query
    question = "Entro quanti giorni arriva il rimborso?"
    answer = rag.query(question, top_k=2)

    print("\n--- RISULTATO DELLA QUERY ---")
    print(f"Domanda: {question}")
    print(f"Risposta: {answer}")

if __name__ == "__main__":
    main()
