# Calcola il vettore di ogni frase in FRASI e confronta con il coseno
# la frase 0 con la 1 (gatto che dorme / cane che dorme), la 0 con la 2
# (gatto / mela), la 2 con la 3 (mela / pera)

import math
from utils import FRASI
from exc_5 import vocabolario
from exc_6 import embedding
from exc_3 import prodotto_scalare
from exc_2 import norma

def coseno(u, v):
    """Calcola la similarità del coseno tra due vettori"""
    denominatore = norma(u) * norma(v)

    if denominatore == 0:
        return 0.0
    return prodotto_scalare(u, v) / denominatore
    

vet = [embedding(f, vocabolario) for f in FRASI]

print(f"Esempio 1: {round(coseno(vet[0], vet[1]), 2)}")
print(f"Esempio 2: {round(coseno(vet[0], vet[2]), 2)}")
print(f"Esempio 3: {round(coseno(vet[2], vet[3]), 2)}")