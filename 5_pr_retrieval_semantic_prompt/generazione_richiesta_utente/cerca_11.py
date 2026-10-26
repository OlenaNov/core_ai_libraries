
# Costruisci l'indice dei DOCUMENTI (un vettore per documento)
# e scrivi cerca(domanda, indice, k) che restituisce i k documenti con punteggio più alto,
# e poi "Entro quanti giorni arriva il rimborso"

from docs_embedding_testo_1 import *
from embedding_richiesta_9 import *
from controlla_compatibilità_10 import *
from operazioni_vettoriali_8 import *

indice = [
    {"id": d["id"], "titolo": d["titolo"], "testo": d["testo"], "vettore": embedding_testo(d["testo"])}
    for d in DOCUMENTI
]

def cerca(domanda, indice, k=2):
    q = embedding_richiesta(domanda)
    risultati = []

    for d in indice:
        controlla_compatibilità(q, d["vettore"])
        risultati.append((prodotto_scalare(q, d["vettore"]), d["id"], d["titolo"]))
        risultati.sort(reverse=True)
        return risultati[:k]

print(len(indice), [len(d["vettore"]) for d in indice])
for punteggio, id_doc, titolo in cerca("Quanto costa la spedizione?", indice, 3):
    print(round(punteggio, 2), id_doc, titolo)

print()

for punteggio, id_doc, titolo in cerca("Entro quanti giorni arriva il rimborso?", indice, 3):
    print(round(punteggio, 2), id_doc, titolo)