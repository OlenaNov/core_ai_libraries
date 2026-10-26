# Traccia. Con gemini-embedding-001 il compito si indica con il parametro task_type. Scrivi config_001(ruolo) 
# che restituisce una configurazione con il tipo corretto per query (RETRIEVAL_QUERY), documento (RETRIEVAL_DOCUMENT) e domanda (QUESTION_ANSWERING). 
# Stampa il tipo di ciascuna.

from init import *
from google.genai import types

RUOLI = {
    "query": "RETRIEVAL_QUERY",
    "documento": "RETRIEVAL_DOCUMENT",
    "domanda": "QUESTION_ANSWERING"
}

def config_001(ruolo):
    return types.EmbedContentConfig(task_type=RUOLI[ruolo])

print([config_001(r).task_type for r in RUOLI])

