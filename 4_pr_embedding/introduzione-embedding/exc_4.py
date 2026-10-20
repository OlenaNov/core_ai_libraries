# Esercizio 1: Il calcolo della Distanza Euclidea
# Questo blocco calcola la "distanza in linea retta" tra due vettori (applicando il teorema di Pitagora multidimensionale). Lo usiamo per confrontare due vettori di embedding (come quelli di "gatto", "cane" e "mela").

import math
from vettori import parole

def distanza(u, v):
    somma = 0
    for n1, n2 in zip(u, v):
        somma += (n1 - n2) ** 2

    return somma ** 0.5 # oppure math.sqrt(somma)

# Test delle distanze
print("Distanza [0,0] e [3,4]:", round(distanza([0, 0], [3, 4]), 2))  # Risultato: 5.0 (Pitagora 3-4-5)
print("Distanza gatto-cane:", round(distanza(parole["gatto"], parole["cane"]), 2))  # Valore basso = molto simili
print("Distanza gatto-mela:", round(distanza(parole["gatto"], parole["mela"]), 2))  # Valore alto = diversi