# •	Le prime tre righe creano il client di Gemini: genai.Client() legge la chiave API dalla variabile d’ambiente. types serve per le configurazioni (negli esercizi seguenti).
# •	MODELLO_TESTO è il modello usato per la generazione.
# •	domanda e contesto sono la domanda di un cliente e un passaggio di documentazione che contiene la risposta, in un formato numerato.


from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()   # usa la chiave nella variabile d'ambiente GEMINI_API_KEY

MODELLO_TESTO = "gemini-3.5-flash"
MODELLO_EMBEDDING = "gemini-embedding-2"
DIM = 768

domanda = "Entro quanti giorni arriva il rimborso?"
contesto = "[1] Il rimborso arriva entro sette giorni dal ricevimento del reso. (fonte: rimborsi.txt)"



def embedding(testo, dim=DIM):
    risultato = client.models.embed_content(
        model=MODELLO_EMBEDDING,
        contents=testo,
        config=types.EmbedContentConfig(output_dimensionality=dim),
    )
    return risultato.embeddings[0].values

def embedding_documento(titolo, testo):
    return embedding(f"title: {titolo} | text: {testo}")

def embedding_domanda(domanda, dim=DIM):
    return embedding(f"task: question answering | query: {domanda}", dim)

CHUNKS = [
    {"id": 0, "fonte": "resi.txt", "testo": "Il reso è gratuito entro quattordici giorni dalla consegna."},
    {"id": 1, "fonte": "rimborsi.txt", "testo": "Il rimborso arriva entro sette giorni dal ricevimento del reso."},
    {"id": 2, "fonte": "spedizioni.txt", "testo": "La spedizione costa cinque euro e la consegna avviene in tre giorni."},
    {"id": 3, "fonte": "pagamenti.txt", "testo": "Si accettano carta di credito e bonifico bancario."},
]

indice = [dict(c, vettore=embedding_documento(c["fonte"], c["testo"])) for c in CHUNKS]

def cerca(domanda, indice, k=2):
    q = embedding_domanda(domanda)
    risultati = []
    for d in indice:
        punteggio = sum(a * b for a, b in zip(q, d["vettore"]))
        risultati.append((punteggio, d))
    risultati.sort(key=lambda x: x[0], reverse=True)
    return risultati[:k]