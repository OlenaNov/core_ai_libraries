
# Per str1 calcola la norma del vettore normalizzato e di quello 
# non normalizzato (normalizza=False). Normalizza a mano il secondo e verifica che 
# coincida con il primo. Poi confronta per str2 e str3, il
# prodotto scalare e il coseno con i vettori normalizzati e non normalizzati.


from math import sqrt
from docs_embedding_testo_1 import *

def norma(v):
    return sqrt(sum(x * x for x in v))

def normalizza(v):
    n = norma(v)
    return [x / n for x in v]

def prodotto_scalare(u, v):
    totale = 0
    for x, y in zip(u, v):
        totale += x * y
    return totale

def coseno(u, v):
    d = norma(u) * norma(v)
    return prodotto_scalare(u, v) / d

def main() -> None:
    str1 = "Come posso restituire un prodotto"
    a = embedding_testo(str1)
    b = embedding_testo(str1, normalizza=False)

    print(round(norma(a), 2), round(norma(b), 2), round(norma(normalizza(b)), 2))
    print(a == normalizza(b))

    str2 = "Il reso è gratuito"
    str3 = "Il reso è rapido"
    n1, n2 = embedding_testo(str2), embedding_testo(str3)
    g1, g2 = embedding_testo(str2, normalizza=False), embedding_testo(str3, normalizza=False)

    print(round(prodotto_scalare(n1, n2), 2), round(coseno(n1, n2), 2))
    print(round(prodotto_scalare(g1, g2), 2), round(coseno(g1, g2), 2))


if __name__ == "__main__":
    main()
