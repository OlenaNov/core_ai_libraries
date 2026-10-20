#Scrivi crea_chunk(doc, fonte, max_car) che restituisce per ogni chunk un dizionario con id, fonte, sezione, posizione, testo e n_caratteri. 
#L’identificativo deve derivare dal contenuto.

#Spiegazione: i metadati dicono da dove viene il chunk (utili per citare la fonte e filtrare). enumerate dà anche la posizione. 
# L’identificativo si ottiene con una funzione di hash (sha1): trasforma il testo in un codice, sempre uguale se il testo è uguale. 
# encode("utf-8") converte la stringa in byte (l’hash lavora su byte), hexdigest() dà il codice in cifre esadecimali e [:8] ne tiene le prime 8. 
# La posizione non entra nella chiave: serve alla prossima prova.
