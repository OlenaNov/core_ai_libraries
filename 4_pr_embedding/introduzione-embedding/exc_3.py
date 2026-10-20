
# Scrivi prodotto_scalare(u, v)
# che moltiplica i numeri nella stessa posizione dei due vettori
# e somma i risultati.

import math

def prodotto_scalare(u, v):
    return sum(a * b for a, b in zip(u, v))

print(prodotto_scalare([1,2,3], [4,5,6]))
print(prodotto_scalare([1,0], [1,0]))