
# Costruisci la matrice documento-termine
# M (5 righe, 25 colonne) e mostra i conteggi di 
#reso, entro, giorni, la in ogni documento e
# la somma di ogni riga
# Con Gemini: costruisci la matrice E degli 
# embedding dei 5 documenti e stampane la
# forma e la matrice delle somiglianze 5*5

from utils_ai import *

m = [vettore_conteggio(d, indici) for d in DOCUMENTI]
print(len(m), len(m[0]))

set_parole = ["reso", "entro", "giorni", "la"]
for p in set_parole:
    print(p.ljust(8), [m[i][indici[p]] for i in range(5)])
    print([sum(riga) for riga in m])

e = embedding_lista(DOCUMENTI)
print(len(e), len(e[0]))
for i in range(5):
    print(([round(coseno(e[i], e[j]), 3) for j in range(5)]))