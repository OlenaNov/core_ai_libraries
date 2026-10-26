from init import *
from config_2 import *

def prepara_documento(contenuto, titolo=None):
    return f"titlr: {titolo or 'none'} | text: {contenuto}"

def prepara_richiesta(testo, modello, ruolo="query"):
    if modello == "gemini-embedding-2":

        contenuto_prefisso = f"query: {testo}" if ruolo == "query" else f"document: {testo}"
        return contenuto_prefisso, None
    elif modello == "gemini-embedding-001":
        return testo, RUOLI.get(ruolo)
    
    raise ValueError(f"Modello sconosciuto: {modello}")


for g in ("gemini-embedding-2", "gemini-embedding-001"):
    print(prepara_richiesta("Come posso pagare?", g))

try:
    prepara_richiesta("x", "Gpt")
except ValueError as e:
    print(e)