# Calcola il vettore del primo chunk con il formato per i 
# documenti. Stampa il testo inviato, la lunghezza del vettore, il
#  tipo dei numeri e la norma. 
#  Poi calcola il vettore di una domanda e verifica che abbia la 
# stessa lunghezza.

from initial import *

chunk = CHUNKS[0]
formato = f"title: {chunk["fonte"]} | text: {chunk["testo"]}"
v = embedding_documento(chunk["fonte"], chunk["fonte"])

print(len(v))
print(type(v[0]).__name__)
print(round(sum(x * x for x in v) ** 0.5, 2))
q = embedding_domanda("Entro quanti giorni posso restituire un prodotto?")
print(len(q), len(q) == len(v))