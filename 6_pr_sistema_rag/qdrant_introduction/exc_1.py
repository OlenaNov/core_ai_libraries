
# Scrivi la funzione verifica_ambiente() che controlla, in 
# un solo dizionario di risultati:
# 1.	quali collezioni esistono in Qdrant 
# (all’inizio nessuna);
# 2.	quanti numeri ha il vettore che Gemini calcola per 
# una frase di prova, e se coincide con DIMENSIONE;
# 3.	cosa risponde il modello di linguaggio a una 
# domanda semplice (“Rispondi con una sola parola: ciao?”).
# Stampa le quattro informazioni: la lista delle collezioni,
#  la lunghezza del vettore, la risposta del modello e
#  il confronto tra lunghezza e DIMENSIONE.

from initial import *

def verifica_ambiente():
    esito = {}
    esito["collezioni"] = [c.name for c in qdrant.get_collections().collections]
    esito["dimensione_embedding"] = len(embedding("prova di connessione"))
    risposta = con_tentativi(lambda: gemini.models.generate_content(
        model=MODELLO_LLM, contents="Rispondi con una sola parola: ciao?"))
    esito["risposta_llm"] = risposta.text.strip()
    return esito


esito = verifica_ambiente()
print(esito["collezioni"])
print(esito["dimensione_embedding"])
print(esito["risposta_llm"])
print(esito["dimensione_embedding"] == DIMENSIONE)



# SPIEGAZIONE FILE PREPARAZIONE ES 1

# •	load_dotenv() e la chiave. Python non legge il .env da solo: load_dotenv() copia le righe del file nelle variabili d’ambiente, e genai.Client() cerca lì GEMINI_API_KEY. La chiave non compare mai nel codice.
# •	QdrantClient(":memory:"). Il database vive solo finché il programma gira, ed è perfetto per esercitarsi. Con path="./qdrant_data" i dati restano su disco, con url="http://localhost:6333" ci si collega a un server vero. Il resto del codice non cambia.
# •	con_tentativi(funzione, tentativi=3, attesa=2). Riceve una funzione e prova a eseguirla fino a 3 volte. Se fallisce, stampa l’errore e aspetta 2 secondi. Al terzo fallimento rilancia l’errore con raise. Si usa spesso con lambda: ..., cioè “una funzione senza nome che non ha parametri”: serve per passare la chiamata senza eseguirla subito. Così i 503 (servizio sovraccarico) non fermano il programma.
# •	embedding_lista(testi, compito=None). Manda a Gemini una lista di testi in una sola chiamata e restituisce la lista dei vettori. compito ottimizza il vettore: "RETRIEVAL_DOCUMENT" per i testi da archiviare, "RETRIEVAL_QUERY" per le domande.
# •	embedding(testo). È la versione per un solo testo: chiama la precedente con una lista di un elemento e prende il primo risultato.


# SPIEGAZIONE  ESERCIZIO


# •	qdrant.get_collections().collections restituisce l’elenco delle collezioni; la comprehension [c.name for c in ...] ne estrae i nomi. In un Qdrant appena creato la lista è vuota.
# •	len(embedding("prova di connessione")) conta i numeri del vettore: 3072. 
# •	La chiamata all’LLM usa gemini.models.generate_content con il modello e il testo della domanda. Il testo generato sta in risposta.text; .strip() toglie spazi e a capo ai bordi. Avvolgere la chiamata in con_tentativi(lambda: ...) la protegge dagli errori temporanei.
# •	Il confronto finale esito["dimensione_embedding"] == DIMENSIONE verifica che la costante usata nel resto del codice coincida con il valore reale: se un giorno cambi modello, il controllo ti avvisa.
# Da ricordare. Un sistema RAG ha tre parti che devono essere d’accordo: il modello di embedding (che produce vettori di una certa dimensione), il database vettoriale (che li archivia) e il modello di linguaggio (che scrive la risposta). Si verifica prima che comunichino.
