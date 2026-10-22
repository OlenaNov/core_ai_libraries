
# Scrivi la funzione inserisci()

from preparazione_1 import *
from intro_db_vettoriali import *

def inserisci(db, id, testo, vettore, meta):
    if id in db:
        raise ValueError(f"id {id} già presente")
    if len(vettore) != DIMENSIONE:
        raise ValueError(f"Dimensione {len(vettore)} invece di {DIMENSIONE}")
    db[id] = {
        "id": id,
        "testo": testo,
        "vettore": vettore,
        "meta": meta
        }

prova = dict(db)
inserisci(prova, 10, "il tablet ha schermo grande", [0.03, 0.04, 0.93], {"categoria": "tecnologia", "anno": 2026})
print(len(prova), len(db))

for args in ((10, "doppione", [0.1, 0.1, 0.8], {}), (11, "troppo corto", [0.5, 0.5], {})):
    try:
        inserisci(prova, *args)
    except ValueError as e:
        print(f"Errore {e}")
        print(len(prova))
    