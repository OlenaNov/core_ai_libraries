
# Calcola il vettore del primo chunk. Stampa la lunghezza, la norma, 
# quante posizioni sono diversi da zero, se il testo in maiuscolo dà lo stesso vettore,
# e la somma del vettore di un testo vuoto.

from initial import *

testo = CHUNKS[0]["testo"]
v = embedding_testo(testo)

print(len(v))
print(round(math.sqrt(sum(x * x for x in v)), 2))
print(sum(1 for x in v if x))
print(v == embedding_testo(testo.upper()))
print(sum(embedding_testo("")))

