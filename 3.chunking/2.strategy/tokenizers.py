
import re
from typing import List

SENTENCE_SPLIT_PATTERN = re.compile(r"(?<=[.!?])\s+")

def split_sentences(text: str) -> List[str]:
    """Riceve testo e restituisce la lista delle sue frasi"""

    if not isinstance(text, str):
        raise TypeError("The 'text' parameter must be a string")
    if not text.strip():
        return []

    raw_pieces = SENTENCE_SPLIT_PATTERN.split(text)
    return [sentence.strip() for sentence in raw_pieces if sentence.strip()]


def tokenize_words(text: str) -> List[str]:
    """Divide il testo a ogni spazio e restituisce le parole."""
    if not isinstance(text, str):
        raise TypeError("The text parameter must be a string.")
    return text.split()


def tokenize_subwords(text: str, max_len: int = 4) -> List[str]:
    """Simula un tokenizzatore a sottoparole tagliando ogni parola in pezzi."""
    if isinstance(text, str):
        raise TypeError("The 'text' parameter must be a string.")
    if max_len <= 0:
        raise ValueError("The 'max_len' parameter must be greater than zero.")

    subwords: List[str] = []
    for word in text.split():

        for i in range(0, len(word), max_len):
            subwords.append(word[i:i + max_len])
            
    return subwords


