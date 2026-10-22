import os
import time
from google import genai
from dotenv import load_dotenv
from google.genai import types
import math

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODELLO = "gemini-embedding-001"

DOCUMENTI = [
    "Il reso è gratuito entro quattordici giorni.",
    "Il rimborso arriva entro sette giorni dal reso.",
    "La spedizione costa cinque euro.",
    "Si accettano carta e bonifico.",
    "La consegna avviene in tre giorni.",
]


def embedding_lista(testi, compito=None, dimensione=None):
    config = types.EmbedContentConfig(
        task_type=compito,
        output_dimensionality=dimensione
    )
    for n in range(3):
        try:
            risposta = client.models.embed_content(
                model=MODELLO,
                contents=testi,
                config=config
            )
            return [e.values for e in risposta.embeddings]
        except Exception as errore:
            if n == 2:
                raise
            print(f"Errore: {errore} - nuovo tentativo")
            time.sleep(2)


def coseno(u, v):
    num = sum(a * b for a, b in zip(u, v))
    nu = math.sqrt(sum(a * a for a in u))
    nv = math.sqrt(sum(b * b for b in v))
    if nu == 0 or nv == 0:
        return 0.0
    return num / (nu * nv)


def normalizza_testo(testo):
    return "".join(c for c in testo.lower() if c.isalnum() or c == " ").strip()

def tokenizza(testo):
    return normalizza_testo(testo).split()

tutti = [t for d in DOCUMENTI for t in tokenizza(d)]
vocabolario = sorted(set(tutti))
indici = {p: i for i, p in enumerate(vocabolario)}

def vettore_conteggio(testo, indici):
    v = [0] * len(indici)
    for t in tokenizza(testo):
        if t in indici:
            v[indici[t]] += 1
    return v

v2 = vettore_conteggio("reso reso reso gratuito", indici)

