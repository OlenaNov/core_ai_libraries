
from utils import *
from exc_5 import vocabolario

def embedding(frase, vocabolario):

    parole = frase.lower().split()

    return [parole.count(p) for p in vocabolario]

v = embedding("Il gatto dorme", vocabolario)
print(f"Vettore della frase: {v}")
print("Somma totale delle occorrenze:", sum(v))

accoppiate = [(p, c) for p, c in zip(vocabolario, v) if c > 0]
print("Parole presenti e conteggi:", accoppiate)

v2 = embedding("Il gatto", vocabolario)
print(v2)
print(sum(v2))
print(([(p,c) for p,c in zip(vocabolario, v2) if c]))