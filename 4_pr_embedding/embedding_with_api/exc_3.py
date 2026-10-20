# Scrivi norma(v): la radice quadrata della somma dei quadrati dei numeri. 
# Provala su [3,4], [1,1], [0,0,0] e su vet[0]

import math
from exc_1 import vet

def norma(v):
    somma = 0
    for x in v:
        somma += x * x

    return math.sqrt(somma)

print(f"{norma([3,4]):.2f}")
print(f"{norma([1,1]):.2f}")
print(f"{norma([0,0,0]):.2f}")
print(f"{norma(vet[0]):.2f}")