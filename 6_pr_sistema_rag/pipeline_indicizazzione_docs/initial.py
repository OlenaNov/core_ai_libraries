
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


#   SPIEGAZIONE
# •	Counter è un contenitore che conta gli elementi.
# •	PAGINE simula un PDF di 3 pagine già estratte come testo. Ogni pagina ha una riga che si ripete (Studio Rossi - Riservato, l’intestazione), il contenuto vero e una riga Pagina N con il numero.

from collections import Counter

PAGINE = [
    "Studio Rossi - Riservato\nCondizioni di reso\nIl reso è gratuito.\nPagina 1",
    "Studio Rossi - Riservato\nSpedizioni\nConsegna in 3 giorni.\nPagina 2",
    "Studio Rossi - Riservato\nPagamenti\nSi accetta carta.\nPagina 3",
]

altre = [
    "Studio Rossi - Riservato\nSezione A\nTesto 1\nPagina 1",
    "Studio Rossi - Riservato\nSezione B\nTesto 2\nPagina 2",
    "Altro Header\nSezione C\nTesto 3\nPagina 3",  # L'intestazione "Studio Rossi" appare solo in 2 pagine su 3
]

#    SPIEGAZIONE 7
   
#    •	Due documenti di prova: RESI, completo, e BOZZA, senza data né versione. OBBLIGATORI elenca i metadati senza i quali un documento non va indicizzato.
# •	separa_intestazione assume la struttura titolo, riga versione/data, corpo: restituisce il titolo (togliendo un eventuale # di Markdown), la riga della versione e il corpo (le righe restanti unite in una sola). Se le righe sono meno di 3, solleva un errore.
# •	estrai_metadati cerca nella riga della versione, con espressioni regolari, una data gg/mm/aaaa (che riordina in formato ISO aaaa-mm-gg) e un numero di versione. Se non li trova usa None.

import re

RESI = "Politica dei resi\nVersione 2.1 - 03/10/2026\nIl reso è gratuito entro quattordici giorni."
BOZZA = "Note interne\nBozza senza data né versione\nTesto da rivedere."
OBBLIGATORI = ("titolo", "data")

def separa_intestazione(testo):
    righe = testo.splitlines()
    if len(righe) < 3:
        raise ValueError("intestazione mancante")
    return righe[0].lstrip("# ").strip(), righe[1].strip(), " ".join(righe[2:])

def estari_metadati(titolo, riga_versione):
    data = re.search(r"(\d{2})/(\d{2})/(\d{4})", riga_versione)
    versione = re.search(r"[Vv]ersione\s+(\d+(?:\.\d+)*)", riga_versione)
    return {
        "titolo": titolo,
        "versione": versione.group(1) if versione else None,
        "data": f"{data.group(3)}-{data.group(2)}.{data.group(1)}" if data else None
    }



#     SPIEGAZIONE

# •	CORPO è il testo di un documento (3 frasi) e METADATI i suoi metadati.
# •	crea_chunk divide il corpo in frasi e le raggruppa in chunk senza superare max_car caratteri: se aggiungere una frase supererebbe il limite, 
# chiude il chunk e ne apre un altro. Per ogni chunk crea un dizionario che eredita i metadati del documento (dict(metadati, ...)) e aggiunge id (doc_id + numero a tre cifre, :03d), 
# doc_id e testo.

CORPO = "Il reso è gratuito entro quattordici giorni dalla consegna. Il prodotto deve essere integro. Il rimborso arriva entro sette giorni."
METADATI = {"fonte": "resi.txt", "titolo": "Politica dei resi", "versione": "2.1"}

def crea_chunk(doc_id, corpo, metadati, max_car=80):
    frasi = [f.strip() + "." for f in corpo.split(".") if f.strip()]
    gruppi, corrente = [], ""
    for frase in frasi:
        if corrente and len(corrente) + 1 + len(frase) > max_car:
            gruppi.append(corrente)
            corrente = frase
        else:
            corrente = (corrente + " " + frase).strip()
    if corrente:
        gruppi.append(corrente)
    return [dict(metadati, id=f"{doc_id}_{i:03d}", doc_id=doc_id, testo=t)
            for i, t in enumerate(gruppi)]

