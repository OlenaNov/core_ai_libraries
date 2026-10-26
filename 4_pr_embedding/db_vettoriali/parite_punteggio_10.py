# Esercizio 10: parità di punteggio e risultati stabili
# Traccia. Se due record hanno lo stesso punteggio, sort(reverse=True) li ordina per id decrescente: un caso sorprendente. 
# Crea un archivio gemelli in cui i record 1 e 2 hanno lo stesso vettore [0.5, 0.5, 0.0] e cerca con [1.0, 1.0, 0.0]. 
# Poi riscrivi cerca in modo che, a parità di punteggio, vinca l’id più basso.

import math
from intro_db_vettoriali import *
from preparazione_1 import *
from ricerca_esatta_9 import *

gemelli= dict(db)
gemelli[1]=dict (db[1],vettore=[0.5, 0.5, 0.0])
gemelli[2]=dict (db[2],vettore=[0.5, 0.5, 0.0])
qq=[1.0, 1.0, 0.0]

print ([(round(s,2),i)for s,i,t in cerca(gemelli,qq,3)])

print ([(round(s,2),i)for s,i,t in cerca(gemelli,qq,3)])
def cerca (db, query, k=3):
    punteggi=[]
    for r in db.values():

        punteggi.append((
            coseno(query, r["vettore"]),
            r["id"],
            r["testo"]
        ))
    punteggi.sort(key=lambda x:(-x[0], x[1]))

    return punteggi [:k]

print ([(round(s,2),i)for s,i,t in cerca(gemelli,qq,3) ])