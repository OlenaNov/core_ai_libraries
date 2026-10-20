
# Scrivi distanza(u, v). Calcola la distanza tra [0,0] e [3,4]. 
# Poi calcola la distanza tra vet[0] e vet[1] (gatto/cane che dormono) e 
# tra vet[0] vet[2] (gatto/mela). Quale è più piccola

from math import sqrt
from exc_1 import vet

def distanza(u, v):
    somma = 0
    for a, b in zip(u, v):
        somma += (a-b) ** 2
        
    return round(sqrt(somma), 4)

print(distanza([0,0], [3,4]))
print(distanza(vet[0], vet[1]))
print(distanza(vet[0], vet[2]))
