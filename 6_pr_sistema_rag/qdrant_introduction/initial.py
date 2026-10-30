
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from qdrant_client import QdrantClient, models

load_dotenv()
gemini = genai.Client()
qdrant = QdrantClient(":memory:")
MODELLO_EMB = "gemini-embedding-001"
MODELLO_LLM = "gemini-flash-lite-latest"    # "gemini-3.8-flash"
DIMENSIONE = 3072
COLLEZIONE = "guida_clienti"


def con_tentativi(funzione, tentativi=3, attesa=2):
    for n in range(tentativi):
        try:
            return funzione()
        except Exception as errore:
            if n == tentativi - 1:
                raise
            print("Errore:", errore, "- nuovo tentativo tra", attesa, "secondi")
            time.sleep(attesa)


def embedding_lista(testi, compito=None):
    config = types.EmbedContentConfig(task_type=compito)
    r = con_tentativi(lambda: gemini.models.embed_content(
        model=MODELLO_EMB, contents=testi, config=config))
    return [e.values for e in r.embeddings]


def embedding(testo, compito=None):
    return embedding_lista([testo], compito)[0]