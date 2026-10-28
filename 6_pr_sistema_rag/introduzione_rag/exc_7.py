
# Scrivi embedding_domanda(domanda, dim=1024) che pulisce la domanda 
# (spazzi in eccesso), rifiuta quella vuota e ne clacola il vettore.
# Scrivi anche controlla_compatibilità(a, b), che solleva un errore se 
# due vettori hanno dimensioni diverse. Provale su una domanda con spazi in eccesso,
# su una domanda vuota e su una domanda a 256 dimensioni confrontata con
# un chunk dell'indice.


from initial import *

def embedding_domanda(domanda, dim=1024):
    domanda = " ".join(domanda.split())
    if not domanda:
        raise ValueError(f"La domanda è vuota")
    return embedding_testo(domanda, dim)

def controlla_compatibilità(a, b):
    if len(a) != len(b):
        raise ValueError(f"Dimensioni diverse: {len(a)} e {len(b)}")
    return True

q = embedding_domanda("Quanto costa la spedizione?")
print(len(q), q == embedding_testo("Quanto costa la spedizione?"))
print(controlla_compatibilità(q, indice[0]["vettore"]))

try:
    embedding_domanda(" ")

except ValueError as e:
    print(e)

try:
    controlla_compatibilità(embedding_domanda("Come posso pagare?", 256), indice[0]["vettore"])

except ValueError as e:
    print(e)