
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


def team_frequency(text: str, word_to_index: Dict[str, int]) -> List[float]:
    """Returns the relative Team Frequency (TF) vector for a text
    (count divided by total number of tokens).
    """
    tokens = tokenize(text)
    total_tokens = len(tokens)

    if total_tokens == 0:
        return [0.0] * len(word_to_index)

    counts = count_vector(text, word_to_index)
    return [count / total_tokens for count in counts]


def to_sparse_vector(vector: List[int]) -> Dict[int, int]:
    """Converts a dense vector into a sparse dictionary,
    retaining only indices and values of non-zero elements.
    """
    return {index: value for index, value in enumerate(vector) if value != 0}


def reconstruct_dense_vector(sparse_dict: Dict[int, int], size: int) -> List[int]:
    """Reconstracts the full dense vector from a sparse dictionary and the original size."""
    dense_vector = [0] * size

    for index, value in sparse_dict.items():
        dense_vector[index] = value

    return dense_vector

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

    # 2. Term Frequency (TF) for DOCUMENTS[1]
    print("--- 2. TERM FREQUENCY (TF) ---")
    target_doc = DOCUMENTS[1]
    tf_vector = team_frequency(target_doc, word_to_index)
    tf_sum = sum(tf_vector)
    print(f"Document 2: \"{target_doc}\"")
    print(f"TF Vector: {[round(x, 4) for x in tf_vector]}")
    print(f"Sum of TF vector components: {tf_sum} (Expected: 1.0)\n")

    # 3. Document-Term Matrix (DTM) and Shape
    print("--- 3. DOCUMENT-TERM MATRIX ---")
    doc_term_matrix = [count_vector(doc, word_to_index) for doc in DOCUMENTS]
    num_rows = len(doc_term_matrix)
    num_cols = len(vocabulary)
    print(f"Matrix Shape -> Rows (Documents): {num_rows}, Columns (Vocabulary): {num_cols}")
    
    words_to_check = ["reso", "entro", "giorni", "la"]
    print("Corpus total occurrences for specific words:")
    for word in words_to_check:
        if word in word_to_index:
            col_idx = word_to_index[word]
            col_sum = sum(doc_vector[col_idx] for doc_vector in doc_term_matrix)
            print(f"  - '{word}': {col_sum}")
    print()

    # 4. Binary Vector (Presence/Multi-hot)
    print("--- 4. BINARY VECTOR (PRESENCE) ---")
    custom_text = "reso reso reso gratuito"
    custom_count_vec = count_vector(custom_text, word_to_index)
    binary_vector = [1 if val > 0 else 0 for val in custom_count_vec]
    print(f"Custom Text: \"{custom_text}\"")
    print(f"Count Vector: {custom_count_vec}")
    print(f"Binary Vector (no repetitions): {binary_vector}\n")

    # 5. Semantic Search Query Example via Cosine Similarity (il tuo codice esistente)
    print("--- 5. SEMANTIC SEARCH QUERY ---")
    query = "Entro quanti giorni posso avere il rimborso?"
    query_vector = count_vector(query, word_to_index)
    
    results: List[Tuple[float, str]] = []
    for i, vec in enumerate(doc_term_matrix):
        similarity = cosine_similarity(query_vector, vec)
        results.append((similarity, DOCUMENTS[i]))

    results.sort(key=lambda x: x[0], reverse=True)

    print(f"Query: \"{query}\"\n")
    print("Sorted results by similarity:")
    for similarity, doc in results:
        print(f"- [{similarity:.4f}] {doc}")

    # 6. Sparse Vector Representation & Reconstruction
    print("--- 6. SPARSE REPRESENTATION (M[1]) ---")
    # Prendiamo M[1] (il secondo documento della matrice documento-termine)
    dense_vector_m1 = doc_term_matrix[1]
    sparse_m1 = to_sparse_vector(dense_vector_m1)
    
    dense_size = len(dense_vector_m1)
    sparse_size = len(sparse_m1)
    
    print(f"Original Document: \"{DOCUMENTS[1]}\"")
    print(f"Full Vector Size: {dense_size}")
    print(f"Sparse Dictionary (non-zero positions): {sparse_m1}")
    print(f"Non-zero elements count: {sparse_size} out of {dense_size}")
    
    # Verifica della ricostruzione
    reconstructed_vector = reconstruct_dense_vector(sparse_m1, dense_size)
    is_identical = (reconstructed_vector == dense_vector_m1)
    print(f"Reconstruction verified successfully? {is_identical}\n")

if __name__ == "__main__":
    main()