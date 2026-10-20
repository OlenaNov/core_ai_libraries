
from utils_ai_gemini import *
from exc_1 import *

def stessa_dimensione(vettori):

    dimensioni = set()

    for v in vettori:
        dimensioni.add(len(v))

    return len(dimensioni) == 1

print(stessa_dimensione([[1,2], [3,4], [5,6]]))
print(stessa_dimensione([[1,2], [3,4,5]]))
print(stessa_dimensione(vet))
print(stessa_dimensione(vet + [[1,2,3]]))