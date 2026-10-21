
# Costruisci ilò vocabolario (l'elenco ordinato delle parole diverse)
# e un dizionario indici che associa a ogni parola la sua posizione.
# Stampa il vocabolario e le posizioni di 
# reso, giorni e il 

from utils import *
from exc_1 import tokenizza

tutti = []

for doc in DOCUMENTI:
    tutti += tokenizza(doc)

vocabolario = sorted(set(tutti))
indice = {
    parola: posizione for posizione, parola in enumerate(vocabolario)
}

print(vocabolario, len(vocabolario))
print(vocabolario.index("reso"), vocabolario.index("giorni"), vocabolario.index("il"))