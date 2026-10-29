
import hashlib, math, re

def embedding_testo(testo, dim=1024):
    v = [0.0] * dim
    for parola in re.findall(r"\w+", testo.lower()):
        posizione = int(hashlib.md5(parola.encode("utf-8")).hexdigest(), 16) % dim
        v[posizione] += 1.0
    n = math.sqrt(sum(x * x for x in v))
    return [x / n for x in v] if n > 0 else v

def normalizza(testo):
    return " ".join(testo.split())

def dividi(testo):
    return [f.strip() + "." for f in testo.split(".") if f.strip()]

def vettorizza(frasi):
    return [embedding_testo(f) for f in frasi]


#    SPIEGAZIONE
# •	tempfile.mkdtemp() crea una cartella temporanea e Path(...) la 
# trasforma in un oggetto percorso. Dentro creiamo una 
# sottocartella faq e 5 file: tre documenti di testo,
# una pagina nella sottocartella e un’immagine logo.png.
# •	write_text(...) scrive un file di testo, write_bytes(...) un 
# file binario. Ogni documento ha tre righe: titolo, riga con 
# versione e data, corpo.
# •	elenca_file cerca ricorsivamente (rglob("*"), anche nelle 
# sottocartelle) e tiene i file (is_file()) la cui estensione 
# (suffix, in minuscolo) è tra quelle ammesse. sorted mette i 
# percorsi in ordine.

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

# •	Due file con lo stesso testo ma codifiche diverse: utf8.txt 
# è scritto in UTF-8, latin.txt in Latin-1 (una codifica più vecchia). 
# Il secondo viene creato come byte, con encode("latin-1").
# •	leggi_testo legge il file dichiarando la codifica UTF-8. 
# Se i byte non sono UTF-8 valido, Python solleva 
# UnicodeDecodeError: la funzione lo intercetta e solleva un 
# ValueError con un messaggio chiaro.

cartella2 = Path(tempfile.mkdtemp())
(cartella2 / "utf8.txt").write_text("Il caffè è incluso.", encoding="utf-8")
(cartella2 / "latin.txt").write_bytes("Il caffè è incluso.".encode("latin-1"))

def leggi_testo(percorso):
    try:
        return percorso.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raise ValueError("codifica non valida (atteso UTF-8)")


import unicodedata

def normalizza_testo(testo):
    testo = unicodedata.normalize("NFC", testo)
    return " ".join(testo.split())


#   SPIEGAZIONE
  
#   •	SPAZIO_NOMI è un valore fisso scelto una volta per tutte: cambiarlo cambierebbe l’identificativo di tutti i documenti.
# •	id_documento calcola con uuid5 un identificativo deterministico a partire dal percorso relativo, ricondotto a forma canonica (senza spazi ai bordi, tutto minuscolo).
# Lo stesso percorso dà sempre lo stesso identificativo.
# •	impronta_testo calcola l’impronta SHA-256 del testo: 64 caratteri esadecimali che cambiano con qualsiasi modifica del contenuto.


import uuid

SPAZIO_NOMI = uuid.UUID("6f1d2c9e-8b34-4a57-9c0e-2d7a41b5e6f3")

def id_documento(percorso_relativo):
    return str(uuid.uuid5(SPAZIO_NOMI, percorso_relativo.strip().lower()))

def impronta_testo(testo):
    return hashlib.sha256(testo.encode("utf-8")).hexdigest()
