#               SPIEGAZIONE
#  •	Le prime tre righe creano il client di Gemini: genai.
# Client() legge la chiave dalla variabile d’ambiente.
# types serve per le configurazioni.
# •	chiamate è un dizionario che conta le chiamate a Gemini.
# •	embedding_documento(titolo, testo) è la funzione che 
# trasforma un chunk in vettore. Aumenta il contatore, poi chiama 
# client.models.embed_content(...) con il testo nel formato per i 
# documenti (title: ... | text: ...) e chiede un vettore di 
# DIM = 768 numeri (output_dimensionality). Il vettore è 
# risultato.embeddings[0].values.
# •	normalizza toglie spazi e a capo in eccesso, 
# dividi taglia il testo a ogni punto e restituisce le frasi, 
# vettorizza calcola il vettore di ogni frase 
# (una chiamata a Gemini per frase).



from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()   # usa la chiave nella variabile d'ambiente GEMINI_API_KEY

MODELLO_EMBEDDING = "gemini-embedding-2"
DIM = 768
chiamate = {"embedding": 0}

def embedding_documento(titolo, testo):
    chiamate["embedding"] += 1
    risultato = client.models.embed_content(
        model=MODELLO_EMBEDDING,
        contents=f"title: {titolo} | text: {testo}",
        config=types.EmbedContentConfig(output_dimensionality=DIM),
    )
    return risultato.embeddings[0].values

def normalizza(testo):
    return " ".join(testo.split())

def dividi(testo):
    return [f.strip() + "." for f in testo.split(".") if f.strip()]

def vettorizza(frasi):
    return [embedding_documento("pipeline", f) for f in frasi]


#   SPIEGAZIONE
# •	tempfile.mkdtemp() crea una cartella temporanea e Path(...) 
# la trasforma in un oggetto percorso. Dentro creiamo una 
# sottocartella faq e 5 file: tre documenti di testo, una pagina 
# nella sottocartella e un’immagine logo.png.
# •	write_text(...) scrive un file di testo, write_bytes(...) 
# un file binario. Ogni documento ha tre righe: titolo, riga con 
# versione e data, corpo.
# •	elenca_file cerca ricorsivamente (rglob("*"), anche nelle 
# sottocartelle) e tiene i file (is_file()) la cui estensione 
# (suffix, in minuscolo) è tra quelle ammesse. sorted ordina i 
# percorsi.


import tempfile
from pathlib import Path

cartella = Path(tempfile.mkdtemp())
(cartella / "faq").mkdir()
(cartella / "resi.txt").write_text("Politica dei resi\nVersione 2.1 - 03/10/2026\nIl reso è gratuito entro quattordici giorni dalla consegna. Il prodotto deve essere integro.", encoding="utf-8")
(cartella / "rimborsi.txt").write_text("Rimborsi\nVersione 1.0 - 15/09/2026\nIl rimborso arriva entro sette giorni dal ricevimento del reso. Il rimborso usa lo stesso metodo di pagamento.", encoding="utf-8")
(cartella / "spedizioni.md").write_text("# Spedizioni\nVersione 1.3 - 01/10/2026\nLa spedizione costa cinque euro. La consegna avviene in tre giorni lavorativi.", encoding="utf-8")
(cartella / "faq" / "pagamenti.txt").write_text("Pagamenti\nVersione 1.1 - 20/09/2026\nSi accettano carta di credito e bonifico bancario.", encoding="utf-8")
(cartella / "logo.png").write_bytes(b"\x89PNG\r\n\x1a\n")

def elenca_file(cartella, estensioni=(".txt", ".md")):
    trovati = []
    for percorso in cartella.rglob("*"):
        if percorso.is_file() and percorso.suffix.lower() in estensioni:
            trovati.append(percorso)
    return sorted(trovati)
