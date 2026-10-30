
# Traccia. Crea i chunk con il limite predefinito (80 caratteri) e 
# stampa id, lunghezza e testo di ciascuno. 
# Mostra quali campi ha il primo chunk e come cambia il numero di chunk 
# con limiti di 200 e 40 caratteri.

from initial import *

chunk = crea_chunk("doc-resi", CORPO, METADATI)
print(len(chunk))

for c in chunk:
    print(c["id"], len(c["testo"]), c["testo"])
print(sorted(chunk[0].keys()))
print(len(crea_chunk("doc-resi", CORPO, METADATI, 200)))
print(len(crea_chunk("doc-resi", CORPO, METADATI, 40)))

#   Spiegazione.
# •	La prima frase (59 caratteri) forma il primo chunk. Aggiungere la seconda porterebbe a 59 + 1 + 32 = 92 caratteri, oltre il limite di 80: il chunk si chiude. Le altre due frasi stanno insieme (32 + 1 + 38 = 71).
# •	Ogni chunk ha sei campi: i tre metadati ereditati (fonte, titolo, versione) più id, doc_id e testo.
# •	L’identificativo del chunk doc-resi_000 contiene quello del documento: da qualsiasi chunk si risale al documento, e si possono trovare tutti i chunk di un documento.
# •	Con un limite di 200 caratteri si ottiene 1 chunk, con 40 se ne ottengono 3 (una frase per chunk).
