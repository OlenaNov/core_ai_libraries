
# Traccia. Scrivi crea_chunk(documenti) che divide ogni documento
#  in frasi e restituisce una lista di chunk, ciascuno con id 
# progressivo, fonte e testo. 
# Stampa quanti chunk risultano, il primo chunk, gli id e le fonti.

from initial import *

def crea_chunk(documenti):
    chunk = []
    for d in documenti:
        for frase in d["testo"].split("."):
            if frase.strip():
                chunk.append({
                    "id": len(chunk),
                    "fonte": d["fonte"],
                    "testo": frase.strip() + "."
                })

    return chunk

chunk = crea_chunk(DOCUMENTI_2)
print(len(chunk))
print(chunk[0])
print([c["id"] for c in chunk])
print([c["fonte"] for c in chunk])