
# scrivi vettore_conteggio(testo, indici)
# che restituisce il vettore di un testo: per ogni parola del vocabolario, quante volte compare. 
# Calcola per DOCUMENTI e per "reso reso reso gratuito"

from utils import *
from exc_5 import *


def vettore_conteggio(testo, indici):
    v = [0] * len(indici)

    for t in tokenizza(testo):
        if t in indici:
            v[indici[t]] += 1

    return v

v = vettore_conteggio(DOCUMENTI[1], indice)
print(v)
print(sum(v))
print([(p, c) for p, c in zip(vocabolario, v) if c])
v2 = vettore_conteggio("reso reso reso gratuito", indice)
print([(p, c) for p, c in zip(vocabolario, v2) if c])