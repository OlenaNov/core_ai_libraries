# Costruisci l'indice: per ogni chunk, un dizionario con anche
# il suo vettore. Poi scrivi aggingi_chunk(indice, fonte, testo)
# che inserisce un nuovo chunk e restituisce il suo id.
# Verifica che tutti i vettori abbiano la stessa dimensione.

from initial import *

indice = [dict(c, vettore = embedding_testo(c["testo"])) for c in CHUNKS]

print(len(indice))
print(list(indice[0].keys()))
print([len(d["vettore"]) for d in indice])

def aggiungi_chunk(indice, fonte, testo):
    nuovo = {
        "id": len(indice),
        "fonte": fonte,
        "testo": testo,
        "vettore": embedding_testo(testo)
    }
    indice.append(nuovo)
    return nuovo["id"]

nuovo_id = aggiungi_chunk(indice, "garanzia.txt", "La garanzia dura due anni.")
print(nuovo_id, len(indice), indice[-1]["fonte"])
print(len(set(len(d["vettore"]) for d in indice)))



