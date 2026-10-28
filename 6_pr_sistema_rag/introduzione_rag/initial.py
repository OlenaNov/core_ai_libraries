
PASSI = [
    ("caricare i documenti", "una volta"),
    ("dividere i documenti in chunk", "una volta"),
    ("calcolare l'embedding di ogni chunk", "una volta"),
    ("salvare i vettori nell'indice", "una volta"),
    ("ricevere la domanda dell'utente", "a ogni domanda"),
    ("calcolare l'embedding della domanda", "a ogni domanda"),
    ("recuperare i chunk più simili", "a ogni domanda"),
    ("costruire il prompt con il contesto", "a ogni domanda"),
    ("generare la risposta con il modello", "a ogni domanda"),
]


# ===> Spiegazione : <===
# modello_finto
#  simula un modello generativo che risponde
#  solo in base ai documenti presenti nel prompt:
# • prompt.splitlines()
#  divide il prompt in righe, e
#  la comprehension tiene quelle che iniziano
#  con [ (le righe del contesto, come [1] testo...);
# • se non ce ne sono, risponde "Non lo so.";
# • altrimenti prende la prima riga,
#  toglie il [1] iniziale con split("] ", 1)[1] e
#  l’eventuale (fonte... finale con split(" (fonte", 1)[0],
#  e restituisce il testo preceduto
#  da "Secondo i documenti: ".


def modello_finto(prompt):
    righe = [r for r in prompt.splitlines() if r.startswith("[")]
    if not righe:
        return "Non lo so."
    testo = righe[0].split("] ", 1)[1].split(" (fonte", 1)[0]
    return "Secondo i documenti: " + testo



# SPIEGAZIONE PREPARAZIONE_3

# DOCUMENTI è la knowledge base: una lista di 4 documenti, ciascuno un 
# dizionario con fonte (il nome del file) e testo.

DOCUMENTI = [
    {"fonte": "resi.txt", "testo": "Il reso è gratuito entro quattordici giorni dalla consegna. Il prodotto deve essere integro."},
    {"fonte": "rimborsi.txt", "testo": "Il rimborso arriva entro sette giorni dal ricevimento del reso."},
    {"fonte": "spedizioni.txt", "testo": "La spedizione costa cinque euro. La consegna avviene in tre giorni lavorativi."},
    {"fonte": "pagamenti.txt", "testo": "Si accettano carta di credito e bonifico bancario."},
]

DOCUMENTI_2 = [
    {"fonte": "resi.txt", "testo": "Il reso è gratuito entro quattordici giorni dalla consegna. Il prodotto deve essere integro."},
    {"fonte": "rimborsi.txt", "testo": "Il rimborso arriva entro sette giorni dal ricevimento del reso. Il rimborso usa lo stesso metodo di pagamento."},
    {"fonte": "spedizioni.txt", "testo": "La spedizione costa cinque euro. La consegna avviene in tre giorni lavorativi."},
]

# La funzione embedding_testo è il nostro modello di embedding.:
# 1.	v = [0.0] * dim crea un vettore di dim zeri (1024 per default).
# 2.	re.findall(r"\w+", testo.lower()) porta il testo in minuscolo ed estrae le parole, ignorando la punteggiatura.
# 3.	Per ogni parola, hashlib.md5(...) calcola un’impronta. int(..., 16) la trasforma in un numero e % dim ne prende il resto della divisione per dim: una posizione tra 0 e 1023. 
# Parole uguali danno sempre la stessa posizione.
# 4.	v[posizione] += 1.0 somma 1 in quella posizione.
# 5.	n è la lunghezza (norma) del vettore e l’ultima riga divide ogni numero per n, così il vettore ha lunghezza 1. Se il vettore è vuoto (n == 0) lo restituisce com’è.
# CHUNKS sono 4 chunk già pronti, uno per documento.


import hashlib, math, re

def embedding_testo(testo, dim=1024):
    v = [0.0] * dim
    for parola in re.findall(r"\w+", testo.lower()):
        posizione = int(hashlib.md5(parola.encode("utf-8")).hexdigest(), 16) % dim
        v[posizione] += 1.0
    n = math.sqrt(sum(x * x for x in v))
    return [x / n for x in v] if n > 0 else v

CHUNKS = [
    {"id": 0, "fonte": "resi.txt", "testo": "Il reso è gratuito entro quattordici giorni dalla consegna."},
    {"id": 1, "fonte": "rimborsi.txt", "testo": "Il rimborso arriva entro sette giorni dal ricevimento del reso."},
    {"id": 2, "fonte": "spedizioni.txt", "testo": "La spedizione costa cinque euro e la consegna avviene in tre giorni."},
    {"id": 3, "fonte": "pagamenti.txt", "testo": "Si accettano carta di credito e bonifico bancario."},
]

indice = [dict(c, vettore=embedding_testo(c["testo"])) for c in CHUNKS]


# per exc. 8 (pr.10)

def cerca(domanda, indice, k=2):
    q = embedding_testo(domanda)
    risultati = []
    for d in indice:
        punteggio = sum(a * b for a, b in zip(q, d["vettore"]))
        risultati.append((punteggio, d))
    risultati.sort(key=lambda r: r[0], reverse=True)
    return risultati[:k]

# per exc. 9 (pr.11)

contesto = ("[1] Il rimborso arriva entro sette giorni dal ricevimento del reso. (fonte: rimborsi.txt)\n"
            "[2] Il reso è gratuito entro quattordici giorni dalla consegna. (fonte: resi.txt)")
domanda = "Entro quanti giorni arriva il rimborso?"
