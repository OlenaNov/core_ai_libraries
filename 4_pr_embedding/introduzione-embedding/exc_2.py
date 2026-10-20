
import math

def norma(v):
    somma = 0
    for x in v:
        somma += x * x

    return math.sqrt(somma)

print(norma([3, 4]))
print(round(norma([1,1]), 2))
print(norma([0,0,0]))