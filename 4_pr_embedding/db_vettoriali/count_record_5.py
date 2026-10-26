# Contare i record per metadato
# Scrivi contaggio_per(db, campo) che restituisce un dizionario con
# quanti record ha ciascun valore di metadato.
# Calcolo per categoria e per anno, e stampa le categorie in
# ordine alfabetico

from intro_db_vettoriali import *

def conteggio_per(db, campo):
    conteggio = {}

    for record in db.values():
        valore = record["meta"][campo]

        conteggio[valore] = conteggio.get(valore, 0) + 1
        return conteggio

print(conteggio_per(db, "categoria"))
print(conteggio_per(db, "anno"))
print(sorted(conteggio_per(db, "categoria")))