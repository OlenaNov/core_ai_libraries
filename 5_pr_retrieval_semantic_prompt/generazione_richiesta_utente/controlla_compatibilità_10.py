
# Scrivi controlla_compatibilità(a, b) che solleva un errore
# se due vettori hanno dimensioni diverse.
# Confronta una richiesta a 128 dimensioni con un documento di 1024,
# poi una richiesta di 1024 con lo stesso documento.

from docs_embedding_testo_1 import *
from embedding_richiesta_9 import *

def controlla_compatibilità(a, b):
    if len(a) != len(b):
        raise ValueError(f"Dimensioni diverse: len(a) e len(b)")
    return True

def main():
    doc = embedding_testo("Si accetano carta di credito e bonifico bancario", 1024)
    q128 = embedding_richiesta("Come posso pagare?", 128)
    print(len(q128), len(doc))

    try:
        controlla_compatibilità(q128, doc)
    except ValueError as e:
        print(e)

    print(controlla_compatibilità(embedding_richiesta("Come posso pagare?"), doc))

if __name__ == "__main__":
    main()