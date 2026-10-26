
# Scrivi embedding richiesta(testo, dim=1024) che pulisce, valida e calcola il vettore della richiesta.
# Provala con spazi attorno al testo con dimensione 128, con una richiesta di soli spazi e 
# verifica che l'esito sia identico al calcolo diretto.

from docs_embedding_testo_1 import *
from valida_richiesta_3 import *
from pulisci_richiesta_2 import *

def embedding_richiesta(testo, dim=1024):
    testo = valida_richiesta(pulisci_richiesta(testo))

    return embedding_testo(testo, dim)

def main():
    str1 = " Come posso pagare? "
    str2 = "Come posso pagare?"
    print(len(embedding_richiesta(str1)))
    print(len(embedding_richiesta(str2, 128)))

    try:
        embedding_richiesta(" ")

    except ValueError as e:
        print(e)

    print(embedding_richiesta(str1))
    print(embedding_richiesta(str1) == embedding_testo(str2))

if __name__ == "__main__":
    main()