
import re
from collections import Counter
from typing import List, Tuple, Dict
from math import sqrt


DOCUMENTS: List[str] = [
    "Il reso è gratuito entro quattordici giorni.",
    "Il rimborso arriva entro sette giorni dal reso.",
    "La spedizione costa cinque euro.",
    "Si accettano carta e bonifico.",
    "La consegna avviene in tre giorni.",
]
REX = r"\b\w+\b"


def normalize_text(text: str) -> str:
    """Normalizes the text by converting it to lowercase."""
    return text.lower()


def tokenize(text: str) -> List[str]:
    """Tokenizes text into a list of words, removing punctuation and normalizing."""
    normalized = normalize_text(text)
    return re.findall(REX, normalized)


def build_vocabulary(documents: List[str]) -> List[str]:
    """Builds and sorted, unique vocabulary list from a collection of documents."""
    vocab =set()

    for doc in documents:
        vocab.update(tokenize(doc))
    return sorted(list(vocab))


def build_word_to_index_map(vocabulary: List[str]) -> Dict[str, int]:
    """Builds a dictionary mapping each word in the vocabulary to its index position"""
    return {word: index for index, word in enumerate(vocabulary)}


def one_hot(word: str, word_to_index: Dict[str, int]) -> List[int]:
    """Returns a One-Hot encoded vector with all zeros and a single 1
    at the position corresponding to the given word in the vocabulary.
    """

    vector = [0] * len(word_to_index)

    if word in word_to_index:
        vector[word_to_index[word]] = 1

    return vector


def count_vector(text: str, word_to_index: Dict[str, int]) -> List[int]:
    """Returns a frequency vector (Bag-of-Words) for a text based on the index dictionary."""
    tokens = tokenize(text)
    vector = [0] * len(word_to_index)

    for token in tokens:
        if token in word_to_index:
            vector[word_to_index[token]] += 1

    return vector


def cosine_similarity(u: List[float], v: List[float]) -> float:
    """Calculates the cosine similarity between two numeric vectors."""

    num = sum(a * b for a, b in zip(u, v))
    nu = sqrt(sum(a * a for a in u))
    nv = sqrt(sum(b * b for b in v))

    if nu == 0 or nv == 0:
        return 0.0

    return num / (nu * nv)


def main() -> None:
    # 1. Vocabulary and Index Dictionary
    vocabulary = build_vocabulary(DOCUMENTS)
    word_to_index = build_word_to_index_map(vocabulary)

    print("--- 1. VOCABULARY & INDEXES ---")
    print(f"Vocabulary ({len(vocabulary)} words): {vocabulary}\n")
    print(f"Index of 'reso': {word_to_index.get('reso')}")
    print(f"Index of 'giorni': {word_to_index.get('giorni')}")
    print(f"Index of 'il': {word_to_index.get('il')}\n")

    # 2. One-Hot Encoding Examples
    print("--- 2. ONE-HOT VECTORS ---")
    one_hot_reso = one_hot("reso", word_to_index)
    one_hot_rimborso = one_hot("rimborso", word_to_index)
    print(f"One-hot for 'reso': {one_hot_reso}")
    print(f"One-hot for 'rimborso': {one_hot_rimborso}\n")

    # 3. Count Vectors (Bag-of-Words via Index Dictionary)
    print("--- 3. COUNT VECTORS ---")
    custom_text = "reso reso reso gratuito"
    print(f"Custom Text: \"{custom_text}\"")
    print(f"Count Vector (Custom Text): {count_vector(custom_text, word_to_index)}\n")

    print("Count Vectors for DOCUMENTS:")
    for i, doc in enumerate(DOCUMENTS):
        vec = count_vector(doc, word_to_index)
        print(f"Doc {i+1}: {vec} -> '{doc}'")
    print()

    # 4. Corpus Statistics & Semantic Search Query Example
    all_tokens: List[str] = []
    for doc in DOCUMENTS:
        all_tokens.extend(tokenize(doc))
    print("--- 4. CORPUS STATS & SIMILARITY SEARCH ---")
    print(f"Total tokens: {len(all_tokens)} | Unique tokens: {len(set(all_tokens))}")
    print(f"Top 5 most frequent words: {Counter(all_tokens).most_common(5)}\n")

    query = "Entro quanti giorni posso avere il rimporso?"
    query_vector = count_vector(query, word_to_index)

    doc_vectors = [count_vector(doc, word_to_index) for doc in DOCUMENTS]

    results: List[Tuple[float, str]] = []

    for i, vec in enumerate(doc_vectors):
        similarity = cosine_similarity(query_vector, vec) 
        results.append((similarity, DOCUMENTS[i]))

    results.sort(key=lambda x: x[0], reverse=True)

    print(f"\nQuery: '{query}'\n")
    print("Sorted results by similarity:")
    for similarity, doc in results:
        print(f"- [{similarity:.4f}] {doc}")

if __name__ == "__main__":
    main()