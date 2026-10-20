#Scrivi crea_chunk(doc, fonte, max_car) che restituisce per ogni chunk un dizionario con id, fonte, sezione, posizione, testo e n_caratteri. 
#L’identificativo deve derivare dal contenuto.

#Spiegazione: i metadati dicono da dove viene il chunk (utili per citare la fonte e filtrare). enumerate dà anche la posizione. 
# L’identificativo si ottiene con una funzione di hash (sha1): trasforma il testo in un codice, sempre uguale se il testo è uguale. 
# encode("utf-8") converte la stringa in byte (l’hash lavora su byte), hexdigest() dà il codice in cifre esadecimali e [:8] ne tiene le prime 8. 
# La posizione non entra nella chiave: serve alla prossima prova.

from utils import *
from chunk_ibrido import *

def crea_chunk(doc, fonte, max_car):

    risultato = []

    for posizione, c in enumerate(chunk_ibrido(doc, max_car)):

        chiave = fonte + "|" + c["titolo"] + "|" + c["testo"]
        id_chunk = hashlib.sha1(chiave.encode("utf-8")).hexdigest()[:8]

        risultato.append({
            "id": id_chunk,
            "fonte": fonte,
            "sezione": c["titolo"],
            "posizione": posizione,
            "testo": c["testo"],
            "n_caratteri": len(c["testo"]),
        })
    return risultato


kb = crea_chunk(DOC, "guida_resi.md", 150)
print(f"\nKB: {kb}")
print(len(kb), "chunk")

for k in kb:
    print(k["id"], k["sezione"], k["posizione"], k["n_caratteri"])
