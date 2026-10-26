
# Calcola il vettore delle parole reso e bonifico
# con dimensioni 2, 4, 8 e 1024, e stampa la lunghezza
# e il prodotto scalare (cioè la somiglianza) tra i due vettori
# Cosa noti?

from docs_embedding_testo_1 import *

for dim in (2, 4, 8, 1024):
    a = embedding_testo("reso", dim)
    b = embedding_testo("bonifico", dim)
    somiglianza = sum(x * y for x, y in zip(a, b))
    print(dim, len(a), round(somiglianza, 2))