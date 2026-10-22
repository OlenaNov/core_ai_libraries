
# Costruisci la lista dei vettori di tutti i documenti
# (la matrice documento-termine) e stampane la forma(righe e colonne).
# Mostra poi, per le parole reso, entro, giorni e la, somma di ogni riga.

from utils import *
from exc_8 import vettore_conteggio
from exc_5 import indice

parole = ["reso", "entro", "giorni", "la"]

m = [vettore_conteggio(d, indice) for d in DOCUMENTI]
print(len(m), len(m[0]))
for p in (parole):
    print(p.ljust(8), [m[i][indice[p]] for i in range(5)])

print([sum(riga) for riga in m])