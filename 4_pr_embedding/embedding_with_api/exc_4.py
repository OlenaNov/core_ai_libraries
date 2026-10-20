
# Scrivi prodotto_scalare(u, v): moltiplica i numeri nella stessa posizione e
# somma i risultati.
# #Prova su [1,2,3], [4,5,6] e su [1,0] con [0,1]. 
# Poi calcola quello di vet[0] con vet[1] e di vet[0] con vet[2]

from exc_1 import vet

def prodotto_scalare(u, v):
    somma = 0

    for n1, n2 in zip(u, v):
        somma += n1 * n2

    return somma

print(f"{prodotto_scalare([1,2,3], [4,5,6]):.3f}")
print(f"{prodotto_scalare([1,0], [0,1]):.3f}")
print(f"{prodotto_scalare(vet[0], vet[0]):.3f}")
print(f"{prodotto_scalare(vet[0], vet[1]):.3f}")
print(f"{prodotto_scalare(vet[0], vet[3]):.3f}")
