# Esercizio 2: Costruire il Vocabolario da una lista di frasi
# Prima di fare gli embeddings, serve un dizionario comune (il vocabolario): l'elenco ordinato e senza doppioni di tutte le parole presenti in un insieme di frasi (FRASI).

from utils import FRASI

vocabolario = sorted({p for f in FRASI for p in f.split()})

print(f"Numero di parole uniche: {len(vocabolario)}")
print(f"Vocabolario: {vocabolario}")