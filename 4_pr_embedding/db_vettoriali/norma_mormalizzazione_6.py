

#Traccia. Scrivi norma(v) (radice della somma dei quadrati) e normalizza(v) (divide ogni numero per la norma, e solleva ValueError per un vettore nullo). 
# Provale su [3, 4] e su [0, 0, 0]. Poi calcola la norma di tutti i vettori dell’archivio, prima e dopo la normalizzazione.

#Spiegazione.
#La norma di [3, 4] è √(9 + 16) = 5. normalizza divide ogni numero per 5 e ottiene [0.6, 0.8], che ha lunghezza 1 e la stessa direzione.
#Un vettore di soli zeri ha norma 0: dividere per zero è impossibile, quindi la funzione solleva un errore invece di restituire un risultato senza senso.
#I vettori dell’archivio hanno norme diverse (da 0,744 a 0,951): sono “lunghi” in modo diverso. Dopo la normalizzazione hanno tutti norma 1,0.


import math
from intro_db_vettoriali import db

def norma(v):
    return math.sqrt(sum(x * x for x in v))

def normalizza(v):
    n = norma(v)
    if n == 0:
        raise ValueError("Vettore nullo: non si può normalizzare")
    return [x / n for x in v]

print(norma([3, 4]), normalizza([3, 4]))
try:
    normalizza([0, 0, 0])
except ValueError as e:
    print(f"Errore: {e}")

print([round(norma(r["vettore"]), 3) for r in db.values()])
print([round(norma(normalizza(r["vettore"])), 3) for r in db.values()])