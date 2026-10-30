# Traccia. Scrivi embedding_batch(chunk) che prima controlla che 
# nessun chunk sia vuoto, poi calcola il vettore di ciascuno e 
# verifica che abbia la dimensione attesa. Applicala ai due chunk
#  validi, controlla dimensioni, norme e chiamate. 
# Poi prova con i tre chunk: l’errore deve arrivare senza
#  spendere chiamate.

from initial import *

def controlla_chunk(chunk):
    for c in chunk:
        if not c ["testo"].strip():
            raise ValueError(f"chunk_vuoto:{c['id']}") 
        
def embedding_batch(chunk):
    controlla_chunk(chunk)
    vettori=[embedding_documento(c["fonte"],c["testo"]) for c in chunk]
    for v in vettori :
        if len(v)!=DIM:
            raise ValueError(f"dimensione in attesa:{len(v)}") 
    return vettori


vettori = embedding_batch(CHUNKS[:2])
print(len(vettori),[len(v) for v in vettori])
print([round(sum(x*x for x in v)**0.5,2)for v in vettori])
print("chiamate:", chiamate["embedding"])

try:
    embedding_batch(CHUNKS)
except ValueError as errore:
    print(errore)
print("chiamate:", chiamate["embedding"])
    


# Spiegazione.
# •	controlla_chunk scorre tutti i chunk e solleva un errore al primo vuoto, prima di chiamare Gemini. È importante: se i chunk fossero controllati uno alla volta, durante la chiamata, i primi due verrebbero calcolati (e pagati) prima di scoprire il terzo difettoso.
# •	embedding_batch calcola il vettore di ogni chunk con la comprehension (una chiamata per chunk) e verifica che la lunghezza sia quella richiesta (DIM = 768).
# •	I due chunk validi producono 2 vettori da 768 numeri con norma 1,0 (vettori di lunghezza 1: la documentazione indica che gemini-embedding-2 normalizza da solo i vettori ridotti). Le chiamate sono 2, una per chunk.
# •	Con i tre chunk l’errore chunk vuoto: doc-vuoto_000 arriva subito e il contatore resta a 2: nessuna chiamata sprecata.
# Con Gemini i numeri stampati (dimensioni, norme, chiamate) dovrebbero coincidere. Se la norma non risultasse 1, controlla la documentazione del modello: per altri modelli (come gemini-embedding-001) i vettori a dimensione ridotta vanno normalizzati a mano.
