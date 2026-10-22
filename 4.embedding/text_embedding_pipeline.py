
"""
Advanced Text Processing, Vocabulary Construction, and Embedding Pipeline
------------------------------------------------
This module implements text preprocessing, tokenization, frequency analysis,
vocabulary indexing. One-Hot encoding, Binary vectors, Term Frequency (TF),
Document-Team Matrices, Embedding matrices, and Gemini-based semantic similarity.
"""

import collections
import logging
import math
import os
import time
from typing import List, Dict, Tuple, Optional
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
)
logger = logging.getLogger(__name__)

# Load enviroment variables
load_dotenv()

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY enviroment variaable is not set.")

# Initialize Gemini Client and Constants
client = genai.Client(api_key=API_KEY)
MODEL_NAME = "gemini-embedding-001"
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2.0

# Document corpus 
DOCUMENTS: List[str] = [
    "Il reso è gratuito entro quattordici giorni.",
    "Il rimborso arriva entro sette giorni dal reso.",
    "La spedizione costa cinque euro.",
    "Si accettano carta e bonifico.",
    "La consegna avviene in tre giorni.",
]


def get_embeddings_batch(
        texts: List[str],
        task_type: Optional[str] = None,
        output_dimensionality: Optional[int] = None
) -> List[List[float]]:
    """
    Generates embedding vectors for a batch of texts with retry logic and error handling,

    Args:
    texts: List of string to embed.
    task_type: Optional task type configuration for the model.
    output_dimensionality: Optional reduced dimensionality for the embeddings.
    
    Returns:
        A list of embedding vectors (lists of floats).
    """
    config = types.EmbedContentConfig(
        task_type=task_type,
        output_dimensionality=output_dimensionality
    )

    for attempt in range(MAX_RETRIES):
        try:
            response = client.models.embed_content(
                model=MODEL_NAME,
                contents=texts,
                config=config
            )

            return [embedding.values for embedding in response.embeddings]

        except Exception as e:
            if attempt == MAX_RETRIES -1:
                logger.e("Max retries reached. Embedding generation failed.")
                raise

            logger.warning(f"Error encountered: {e}. Nuovo tentativo in corso...")
            time.sleep(RETRY_DELAY_SECONDS)


def calculate_cosine_similarity(u: List[float], v: List[float]) -> float:
    """
    Calculates the cosine similarity between two numeric vectors.

    Args:
        u: First vector.
        v: Second vector.

    Returns:
        Cosine similarity score as a float between -1.0 and 1.0
    """
    dot_product = sum(a * b for a, b in zip(u, v))
    norm_u = math.sqrt(sum(a * a for a in u))
    norm_v = math.sqrt(sum(b * b for b in v))

    if norm_u == 0.0 or norm_v == 0.0:
        return 0.0

    return dot_product / (norm_u * norm_v)


def normalize_text(text: str) -> str:
    """
    Normalizes input text by converting to lowercase, removing punctuation,
    and stripping extra whitespace.

    Args:
        text: Raw input string.

    Returns:
    Cleaned and normalized string.
    """

    cleaned_chars = [c for c in text.lower() if c.isalnum() or c == " "]
    return "".join(cleaned_chars).strip()


def tokenize_text(text: str) -> List[str]:
    """
    Tokenizes normalized text into a list of words.

    Args:
        text: Input string.

    Returns: 
        List of string tokens.
    """
    return normalize_text(text).split()


def build_vocabulary(documents: List[str]) -> Tuple[List[str]]:
    """
    Builds a unique sorted vocabulary list and a word-to-index mapping dictionary
    
    Args:
        documents: List of raw text documents.

    Returns: 
        A tuple containing:
            - Vocabulary list (sorted unique words)
            - Dictionary mapping words to integer indices
    """
    all_tokens = []
    for doc in documents:
        all_tokens.extend(tokenize_text(doc))

    vocab = sorted(set(all_tokens))
    vocab_to_index = {word: idx for idx, word in enumerate(vocab)}
    return vocab, vocab_to_index


def generate_one_hot_vector(word: str, vocab_to_index: Dict[str, int]) -> List[int]:
    """
    Generates a One-Hot encoded binary vector for a given word based on vocabulary indices.
    """
    vector = [0] * len(vocab_to_index)
    if word in vocab_to_index:
        vector[vocab_to_index[word]] = 1

    return vector


def generate_binary_vector(text: str, vocab_to_index: Dict[str, int]) -> List[int]:
    """
    Generates a binary presence/absence vector for a text string.
    """
    vector = [0] * len(vocab_to_index)
    tokens = tokenize_text(text)
    for token in tokens:
        if token in vocab_to_index:
            vector[vocab_to_index[token]] = 1
    return vector


def generate_count_vector(text: str, vocab_to_index: Dict[str, int]) -> List[int]:
    """
    Generates a Term Frequency (Bag-of-Words count) vector for a text string.
    """
    vector = [0] * len(vocab_to_index)
    tokens = tokenize_text(text)
    for token in tokens:
        if token in vocab_to_index:
            vector[vocab_to_index[token]] += 1
    return vector


def calculate_tf(text: str, vocab_to_index: Dict[str, int]) -> List[float]:
    """
    Calculates the Term Frequency (TF) normalized vector where values sum to 1.0.
    """
    vector = [0.0] * len(vocab_to_index)
    tokens = tokenize_text(text)
    total_tokens = len(tokens)

    if total_tokens == 0:
        return vector

    for token in tokens:
        if token in vocab_to_index:
            vector[vocab_to_index[token]] += 1.0

    return [count / total_tokens for count in vector]


def main() -> None:
    """Main execution pipeline for NLP representation, matrices and embeddings."""

# 1. Vocabulary and Indexing
    vocabulary, vocab_indices = build_vocabulary(DOCUMENTS)
    vocab_size = len(vocabulary)
    print(f"--- Vocabolario del Corpus (Dimensione: {vocab_size}) ---")
    print(vocabulary)

    # 2. Vettori a Conteggio e Confronti
    print("\n--- Vettori a Conteggio (Bag-of-Words) ---")
    doc1_count_vector = generate_count_vector(DOCUMENTS[1], vocab_indices)
    custom_count_vector = generate_count_vector("reso reso reso gratuito", vocab_indices)
    
    print(f"Conteggi per DOCUMENTS[1]: {doc1_count_vector}")
    print(f"Conteggi per 'reso reso reso gratuito': {custom_count_vector}")

    # Confronto Count Vector vs Embedding di DOCUMENTS[1]
    doc1_embedding = get_embeddings_batch([DOCUMENTS[1]])[0]
    non_zero_count = sum(1 for val in doc1_count_vector if val > 0)
    print(f"Vettore a conteggio: {len(doc1_count_vector)} dimensioni (di cui {non_zero_count} non zero)")
    print(f"Embedding denso Gemini: {len(doc1_embedding)} dimensioni (tutte non zero)")

    # 3. Vettori Binari e Confronti di Similarità (Frasi di prova)
    print("\n--- Confronto tra 'reso reso reso gratuito' e 'reso gratuito' ---")
    phrase_a = "reso reso reso gratuito"
    phrase_b = "reso gratuito"

    # A) Tramite Conteggi
    count_a = generate_count_vector(phrase_a, vocab_indices)
    count_b = generate_count_vector(phrase_b, vocab_indices)
    sim_counts = calculate_cosine_similarity(count_a, count_b)

    # B) Tramite Vettori Binari
    bin_a = generate_binary_vector(phrase_a, vocab_indices)
    bin_b = generate_binary_vector(phrase_b, vocab_indices)
    sim_binary = calculate_cosine_similarity(bin_a, bin_b)

    # C) Tramite Embedding Gemini
    emb_phrases = get_embeddings_batch([phrase_a, phrase_b])
    sim_embedding = calculate_cosine_similarity(emb_phrases[0], emb_phrases[1])

    print(f"Similarità Coseno (Vettori a Conteggio): {round(sim_counts, 2)}")
    print(f"Similarità Coseno (Vettori Binari): {round(sim_binary, 2)}")
    print(f"Similarità Coseno (Embedding Gemini): {round(sim_embedding, 2)}")

    # 4. Matrice Documento-Termine (M)
    print("\n--- Matrice Documento-Termine (M) ---")
    document_term_matrix = [generate_count_vector(doc, vocab_indices) for doc in DOCUMENTS]
    
    target_words_to_inspect = ["reso", "entro", "giorni", "la"]
    print(f"{'Documento':<45} | " + " | ".join([f"{w:>6}" for w in target_words_to_inspect]) + " | {'Somma Riga'}")
    print("-" * 80)
    for i, doc in enumerate(DOCUMENTS):
        row_counts = document_term_matrix[i]
        word_counts_str = " | ".join([f"{row_counts[vocab_indices[w]]:>6}" if w in vocab_indices else f"{0:>6}" for w in target_words_to_inspect])
        row_sum = sum(row_counts)
        print(f"Doc {i+1}: {doc[:40]:<38} | {word_counts_str} | {row_sum:>10}")

    # 5. Matrice di Embedding dei Documenti (E) e Matrice di Similarità 5x5
    print("\n--- Matrice Embedding (E) e Matrice di Similarità 5x5 ---")
    embedding_matrix = get_embeddings_batch(DOCUMENTS)
    print(f"Forma della matrice E degli embedding: ({len(embedding_matrix)}, {len(embedding_matrix[0])})")

    print("\nMatrice di Similarità Coseno (5x5 fra i documenti):")
    similarity_matrix_5x5 = []
    for u in embedding_matrix:
        row_sims = [round(calculate_cosine_similarity(u, v), 2) for v in embedding_matrix]
        similarity_matrix_5x5.append(row_sims)
    
    for row in similarity_matrix_5x5:
        print(row)

    # 6. Term Frequency (TF) e Test Raddoppio Documento
    print("\n--- Term Frequency e Test Raddoppio Documento ---")
    doc_target = DOCUMENTS[1]
    tf_vector = calculate_tf(doc_target, vocab_indices)
    tf_sum = sum(tf_vector)
    print(f"Somma degli elementi del vettore TF per DOCUMENTS[1]: {tf_sum} (Verificato == 1.0)")

    # Duplicazione documento: d + " " + d
    duplicated_doc = doc_target + " " + doc_target
    tf_orig = calculate_tf(doc_target, vocab_indices)
    tf_dup = calculate_tf(duplicated_doc, vocab_indices)
    sim_tf_dup = calculate_cosine_similarity(tf_orig, tf_dup)

    emb_orig_dup = get_embeddings_batch([doc_target, duplicated_doc])
    sim_emb_dup = calculate_cosine_similarity(emb_orig_dup[0], emb_orig_dup[1])

    print(f"Testo originale: '{doc_target}'")
    print(f"Testo raddoppiato: '{duplicated_doc}'")
    print(f"Similarità Coseno TF (Originale vs Raddoppiato): {sim_tf_dup}")
    print(f"Similarità Coseno Embedding Gemini (Originale vs Raddoppiato): {round(sim_emb_dup, 2)}")

if __name__ == "__main__":
    main()