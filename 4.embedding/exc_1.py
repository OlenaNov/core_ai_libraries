# Ricerca Semantica con similarità del coseno
# Dato un elenco di documenti e una query dell'utente, 
# calcolare gli embeddings (simulati o reali) e trovare il documento più 
# semanticamente affine usando la similarità del coseno.

import numpy as np

documents = [
    "La pizza margherita è il piatto tipico di Napoli.",
    "Il machine learning e il deep learning guidano l'intelligenza artificiale.",
    "Le auto elettriche riducono le emissioni di CO2 in città."
]

query = "Intelligenza artificiale e reti neurali"

def get_fake_embedding(text: str) -> list[float]:

    if "intelligenza" in text.lower() or "learning" in text.lower():
        return [0.9, 1.0, 0.1]
    elif "pizza" in text.lower():
        return [0.1, 0.9, 0.1]
    else:
        return [0.1, 0.1, 0.9]

def cosine_similarity(v1, v2):
    """Calcola la similarità del coseno tra due vettori."""
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

query_vector = get_fake_embedding(query)

best_score = -1
best_doc = None

for doc in documents:
    doc_vector = get_fake_embedding(doc)
    score = cosine_similarity(query_vector, doc_vector)
    print(f"Score per '{doc[:30]}...': {score:.2f}")

    if score > best_score:
        best_score = score
        best_doc = doc

print(f"\nRisultato più rilevante: '{best_doc}' (Score: {best_score:.2f})")
