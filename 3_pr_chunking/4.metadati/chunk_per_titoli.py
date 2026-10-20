# Scrivi chunk_per_titoli(testo) che restituisce una lista di dizionari con titolo e testo di ogni sezione.
# Provala su DOC.
# Spiegazione: la funzione legge il documento riga per riga: a ogni riga che inizia con # chiude 
# la sezione precedente (se ha del testo) e ricorda il nuovo titolo.
# Il titolo principale Guida ai resi non ha testo sotto e non produce una sezione.
# È la suddivisione più naturale, perché segue la struttura scelta dall’autore,
# ma le sezioni possono essere troppo lunghe.
from utils import *

def chunk_per_titoli(testo):

    sezioni, titolo, righe = [], None, []

    for riga in testo.splitlines():

        if riga.startswith("#"):
            if "".join(righe).strip():
                sezioni.append({
                    "titolo": titolo,
                    "testo": "\n".join(righe).strip()
                })
                
            titolo = riga.lstrip("# ")
            righe = []
        else:
            righe.append(riga)
            
    if "".join(righe).strip():
        sezioni.append({
            "titolo": titolo,
            "testo": "\n".join(righe).strip()
        })
    return sezioni

sez = chunk_per_titoli(DOC)
print([(s["titolo"], len(s["testo"])) for s in sez])