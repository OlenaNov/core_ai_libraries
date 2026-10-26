# La ricerca esatta dei primi k
# Scrivi cerca(db, query, k=3) che confronta la domanda
# con tutti i record e restituisce i l più simili come 
# tuple(punteggio, id, testo), dal più simile al meno simile.
# Provala con [0.9, 0.1, 0.0]
# (k=3) e con [0.1, 0.1, 0.9] (k = 2, stampando solo gli id).

import math
from intro_db_vettoriali import *
from preparazione_1 import *

def cerca(db, query, k=3):

    punteggi = []
    for r in db.values():
        punteggi.append((coseno(query, r["vettore"]), r["id"], r["testo"]))

        punteggi.sort(reverse=True)

    return punteggi[:k]

for s, i, t in cerca(db, [0.9, 0.1, 0.0]):
    print(round(s, 3), i, t)
    print([i for s, i, t in cerca(db, [0.1, 0.1, 0.9], 2)])