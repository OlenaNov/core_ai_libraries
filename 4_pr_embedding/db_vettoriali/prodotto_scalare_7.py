
#Esercizio 7: coseno, prodotto scalare e distanza
# Traccia. Scrivi prodotto_scalare(u, v) e distanza(u, v) (distanza euclidea). 
# Prendi la domanda q = [0.9, 0.1, 0.0] e tre candidati: A = [1.8, 0.2, 0.0] (stessa direzione di q, lunghezza doppia),
# B = [0.45, 0.05, 0.0] (stessa direzione, lunghezza metà) e il vettore del record 1. 
# Per ciascuno stampa coseno, prodotto scalare e distanza.

from preparazione_1 import *
from intro_db_vettoriali import *

def prodotto_scalare(u, v):
    return sum(a * b for a, b in zip(u, v))

def distanza(u, v):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(u, v)))

q = [0.9, 0.1, 0.0]

candidati = [("A doppio", [1.8,0.2,0.0]),
             ("B metà", [0.45,0.05,0.0]),
             ("id 1", db[1]["vettore"]),             
             ]

for nome, v in candidati:
    print(nome.ljust(9), round(coseno(q, v), 2), round(prodotto_scalare(q, v), 2), round(distanza(q, v), 2))