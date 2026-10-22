
#SPIEGAZIONE

#import math carica il modulo matematico: serve math.sqrt (radice quadrata) per il coseno.
#DIMENSIONE = 3 è la lunghezza che deve avere ogni vettore dell’archivio.
# Un archivio accetta solo vettori della stessa dimensione.
#DOCUMENTI è una lista di 9 record su tre argomenti: animali (id 1-3), cibo (4-6), 
# tecnologia (7-9). Ogni record è un dizionario con quattro campi: id, testo, 
# vettore e meta (i metadati, a loro volta un dizionario con categoria e anno).
#I vettori hanno 3 numeri inventati per l’esercizio: 
# la prima posizione si può leggere come “quanto parla di animali”,
# la seconda “di cibo”, la terza “di tecnologia”. 
# Nei modelli veri le dimensioni sono centinaia o migliaia e non hanno un’etichetta leggibile.
# Il documento 9 (il robot che impara dai dati) ha un valore non trascurabile anche sugli animali:
# servirà negli esercizi 17 e 18.
#coseno(u, v) misura quanto due vettori puntano nella stessa direzione, da 0 (nulla in comune) a 1 (stessa direzione).
# Passo per passo: zip(u, v) accoppia i numeri nella stessa posizione 
# e il ciclo ne somma i prodotti (il prodotto scalare num). 
# nu e nv sono le lunghezze (norme) dei due vettori. 
# Se uno dei due ha lunghezza zero la funzione restituisce 0.0, 
# per evitare la divisione per zero. Altrimenti restituisce num / (nu * nv).


import math

DIMENSIONE = 3

DOCUMENTI = [
    {"id": 1, "testo": "il gatto dorme sul divano",
     "vettore": [0.92, 0.05, 0.03], "meta": {"categoria": "animali", "anno": 2022}},
    {"id": 2, "testo": "il cane corre nel parco",
     "vettore": [0.88, 0.04, 0.08], "meta": {"categoria": "animali", "anno": 2023}},
    {"id": 3, "testo": "il pappagallo impara a parlare",
     "vettore": [0.80, 0.02, 0.18], "meta": {"categoria": "animali", "anno": 2024}},
    {"id": 4, "testo": "la pasta al pomodoro è pronta",
     "vettore": [0.05, 0.93, 0.02], "meta": {"categoria": "cibo", "anno": 2022}},
    {"id": 5, "testo": "la mela è un frutto dolce",
     "vettore": [0.10, 0.88, 0.02], "meta": {"categoria": "cibo", "anno": 2023}},
    {"id": 6, "testo": "il pane fresco profuma",
     "vettore": [0.03, 0.90, 0.07], "meta": {"categoria": "cibo", "anno": 2024}},
    {"id": 7, "testo": "il computer si avvia piano",
     "vettore": [0.02, 0.03, 0.95], "meta": {"categoria": "tecnologia", "anno": 2022}},
    {"id": 8, "testo": "il telefono ha una nuova batteria",
     "vettore": [0.04, 0.06, 0.90], "meta": {"categoria": "tecnologia", "anno": 2023}},
    {"id": 9, "testo": "il robot impara dai dati",
     "vettore": [0.30, 0.02, 0.68], "meta": {"categoria": "tecnologia", "anno": 2024}},
]


def coseno(u, v):
    num = 0
    for a, b in zip(u, v):
        num += a * b
    nu = math.sqrt(sum(a * a for a in u))
    nv = math.sqrt(sum(b * b for b in v))
    if nu == 0 or nv == 0:
        return 0.0
    return num / (nu * nv)
