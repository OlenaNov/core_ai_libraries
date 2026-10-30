# Traccia. In Qdrant i vettori stanno dentro una collezione, che 
# deve dichiarare in anticipo quanti numeri ha ogni vettore e con 
# quale misura confrontarli. 
# Scrivi crea_collezione(nome, dimensione) che:
# 1.se la collezione esiste già, la cancella, così la funzione si
#  può rilanciare;
# 2.la crea con vettori di dimensione numeri e distanza coseno.
# Poi: crea COLLEZIONE, stampa dimensione e distanza lette da
#  get_collection e il numero di punti; ricreala e verifica che 
# ne esista una sola; prova a inserire un punto con un vettore di 
# soli 3 numeri e cattura l’errore; stampa infine il numero di 
# punti.

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
    



# •	qdrant.collection_exists(nome) risponde True o False. Se la collezione esiste, delete_collection la elimina: così crea_collezione si può eseguire più volte senza errori. Attenzione: cancellare una collezione cancella anche i suoi dati.
# •	create_collection riceve due cose: il nome e vectors_config. models.VectorParams(size=..., distance=...) dice che ogni vettore ha size numeri e che si confrontano con la distanza coseno (Distance.COSINE). Altre scelte possibili sono prodotto scalare, distanza euclidea e Manhattan. Per gli embedding di testo si usa di norma il coseno.
# •	get_collection(nome) restituisce la configurazione: info.config.params.vectors.size è 3072 e points_count è 0, cioè la collezione è vuota.
# •	Ricreare la collezione dà ancora una sola collezione, guida_clienti: la prima viene cancellata e rifatta.
# •	Il try ... except Exception serve a vedere che Qdrant rifiuta un vettore di dimensione sbagliata: la collezione vuole 3072 numeri e ne riceve 3. Stampiamo solo il nome del tipo di errore (type(errore).__name__), perché cambia tra modalità memoria (ValueError) e server (un errore HTTP). Il punto non entra: count(..., exact=True).count resta 0.
