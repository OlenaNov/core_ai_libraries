
# Costruisci l'indice: per ogni chunk, un dizionario che contiene anche
# il suo vettore (calcolato con Gemini). Poi scrivi aggingi_chunk(indice, fonte, testo) 
# che inserisce un nuovo chunk e restituisce il suo id. Verifica che tutti i vettori abbiano
# la stessa dimensione.

from initial import *

indice = [dict(c, vettore=embedding_documento(c["fonte"], c["testo"])) for c in CHUNKS]

print(len(indice))
print(list(indice[0].keys()))
print([len(d["vettore"]) for d in indice])

def aggiungi_chunk(indice, fonte, testo):
    nuovo = {
        "id": len(indice),
        "fonte": fonte,
        "testo": testo,
        "vettore": embedding_documento(fonte, testo)
    }
    indice.append(nuovo)
    return nuovo["id"]

nuovo_id = aggiungi_chunk(indice, "garanzia.txt", "La garanzia dura 2 anni.")
print(nuovo_id, len(indice), indice[-1]["fonte"])
print(len(set(len(d["vettore"]) for d in indice)))
