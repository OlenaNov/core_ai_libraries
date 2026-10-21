
# Scrivi one_hot(parola, indici) che restituisce un vettore 
# con tutti zeri e un solo 1 nella posizione della parola.
# Calcola quello di reso e rimboro

from exc_5 import *
from utils import *

def one_hot(parola, indici):
    vettore = [0] * len(indici)
    vettore[indici[parola]] = 1
    return vettore

one = one_hot("reso", indice)
print(one)
print(sum(one), one.index(1))
print(coseno(one_hot("reso", indice), one_hot("rimborso", indice)))
print(coseno(one, one))