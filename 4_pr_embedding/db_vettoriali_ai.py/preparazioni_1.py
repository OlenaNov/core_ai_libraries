# TODO!!!

import math
import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client()
MODELLO = "gemini-embedding-001"
DIMENSIONE = 3072

DOCUMENTI = [
    {"id": 1, "testo": "il gatto dorme sul divano",
     "meta": {"categoria": "animali", "anno": 2022}},
    {"id": 2, "testo": "il cane corre nel parco",
     "meta": {"categoria": "animali", "anno": 2023}},
    {"id": 3, "testo": "il pappagallo impara a parlare",
     "meta": {"categoria": "animali", "anno": 2024}},
    {"id": 4, "testo": "la pasta al pomodoro è pronta",
     "meta": {"categoria": "cibo", "anno": 2022}},
    {"id": 5, "testo": "la mela è un frutto dolce",
     "meta": {"categoria": "cibo", "anno": 2023}},
    {"id": 6, "testo": "il pane fresco profuma",
     "meta": {"categoria": "cibo", "anno": 2024}},
    {"id": 7, "testo": "il computer si avvia piano",
     "meta": {"categoria": "tecnologia", "anno": 2022}},
    {"id": 8, "testo": "il telefono ha una nuova batteria",
     "meta": {"categoria": "tecnologia", "anno": 2023}},
    {"id": 9, "testo": "il robot impara dai dati",
     "meta": {"categoria": "tecnologia", "anno": 2024}},
]


def embedding_lista(testi, compito=None, dimensione=None):
    config = types.EmbedContentConfig(
        task_type=compito, output_dimensionality=dimensione
    )
    for n in range(3):
        try:
            r = client.models.embed_content(
                model=MODELLO, contents=testi, config=config
            )
            return [e.values for e in r.embeddings]
        except Exception as errore:
            if n == 2:
                raise
            print("Errore:", errore, "- nuovo tentativo")
            time.sleep(2)
