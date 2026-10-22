
"""
Embedding Pipeline and Text Normalization Utility
------------------------------------------------
This module implements robust text preprocessing, tokenization,
batch embedding generation via Google GenAI, and vector similarity metrics.
"""
import logging
import math
import os
import time
from typing import List, Optional
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
    Nurmalises input text by converting to lowercase, removing punctuation,
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


def main() -> None:
    """Main execution pipeline for testing tokenization, normalizzation and embeddings."""

    # 1. Tokenization and Length Analysis
    print("--- Test Tokenizzazione e Dimensioni Vettoriali ---")
    print(tokenize_text(DOCUMENTS[0]))
    print([len(tokenize_text(doc)) for doc in DOCUMENTS])

    vectors = get_embeddings_batch(DOCUMENTS)
    print(len(vector) for vector in vectors)

    # 2. Text Normalization & Cosine Similarity Comparison
    print("\n--- Test Normalizzazione e Similarità Coseno ---")
    test_string = " Reso GRATUITO!!! Entro 14 giorni, sempre."
    test_string_2 = "L'uomo è qui."

    print(normalize_text(DOCUMENTS[1]))
    print(normalize_text(test_string))
    print(normalize_text(test_string_2))

    # Compare raw vs normalized text string embeddings
    similarity_vectors_1 = get_embeddings_batch([test_string, normalize_text(test_string)])
    print(f"Cosine similarity (DOCUMENTS[1] vs normalized): {round(calculate_cosine_similarity(similarity_vectors_1[0], similarity_vectors_1[1]), 2)}")

    # Compare raw vs normalized document embeddings
    similarity_vectors_2 = get_embeddings_batch([DOCUMENTS[1], normalize_text(DOCUMENTS[1])])
    print(f"Cosine similarity (DOCUMENTS[1] vs normalized): {round(calculate_cosine_similarity(similarity_vectors_2[0], similarity_vectors_2[1]), 2)}")


if __name__ == "__main__":
    main()