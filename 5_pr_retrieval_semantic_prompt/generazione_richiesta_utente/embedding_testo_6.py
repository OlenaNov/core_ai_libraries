
# Calcola con embedding_testo il vettore di str1.
# Stampa la lunghezza il tipo dei numeri, quante posizioni
# sono diverse da zero e i valori diversi presenti.
# Poi verifica che scrivere la stessa richiesta in modo diverso
# es. str2 dia lo stesso vettore, e controlla il caso di un testo vuoto

str1= "Come posso restituire un prodotto?"
str2 = "come posso restituire un PRODOTTO"

from docs_embedding_testo_1 import *

v = embedding_testo(str1)
print(len(v))
print(type(v[0]).__name__)
print(sum(1 for x in v if x))
print(sorted({round(x, 3) for x in v}))

v2 = embedding_testo(str2)
print(v == v2)
print(sum(embedding_testo("")))