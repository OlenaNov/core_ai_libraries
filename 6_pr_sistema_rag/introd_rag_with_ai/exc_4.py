
# prepara_domanda(domanda) che toglie gli spazzi in eccesso e rifiuta la domanda vuota 
# e controlla_compatibilita(a, b) che solleva un errore se due vettori hanno dimensioni diverse.
# Provale su una domanda con spazi in eccesso, su una domanda vuota e su una domanda incorporata a 256 dimensioni e confrontata con un chunk dell’indice.


from initial import *

def prepara_domanda(domanda):
    domanda = " ".join(domanda.split())
    if not domanda:
        raise ValueError("La domanda è vuota.")
    return domanda

def controlla_compatibilità(a, b):
    if len(a) != len(b):
        raise ValueError(f"Dimensioni diverse: {len(a)} e {len(b)}.")
    return True

q = embedding_domanda(prepara_domanda("Quanto costa la spedizione?"))
print(len(q))
print(controlla_compatibilità(q, indice[0]["vettore"]))

try:
    prepara_domanda(" ")
except ValueError as e:
    print(e)

try: 
    controlla_compatibilità(embedding_domanda("Come posso pagare?", 256), indice[0]["vettore"])
except ValueError as e:
    print(e)