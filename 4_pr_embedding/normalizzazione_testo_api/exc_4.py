
# Costruisci il vocabolario e il dizionario indici.
# Stampa il vocabolario e le posizioni di reso, giorni e il.
# Con Gemini: Costruisci il dizionario emb_parole che associa a ogni parola
# il suo vettore e cosa restituisce per reso.

from utils_ai import *

vocabolario = sorted(set(tutti))
indice = {p: i for i, p in enumerate(vocabolario)}

print(len(vocabolario))
print(vocabolario)
print(indice["reso"])
print(indice["giorni"])
print(indice["il"])

emb_parole = dict(zip(vocabolario, embedding_lista(vocabolario)))

print(len(emb_parole))
print(indice["reso"])
print(len(emb_parole["reso"]))
print([round(x, 4) for x in emb_parole["reso"][:3]])