
#Che cosa fa la preparazione
#Gli import.
# •	hashlib fornisce md5, una funzione che trasforma un testo in un numero sempre uguale per lo stesso testo.
# •	math serve per la radice quadrata (math.sqrt).
# •	re fornisce le espressioni regolari, usate per dividere il testo in parole.
# La funzione embedding_testo(testo, dim=1024, normalizza=True) è il nostro modello di embedding. Riceve un testo e restituisce un vettore di dim numeri.
# 1.	v = [0.0] * dim crea un vettore di dim zeri.
# 2.	re.findall(r"\w+", testo.lower()) porta il testo in minuscolo e ne estrae le parole, ignorando la punteggiatura (\w+ significa “una o più lettere o cifre”).
# 3.	Per ogni parola, md5 calcola un numero. numero % dim è il resto della divisione per dim: un numero tra 0 e dim - 1. È la posizione del vettore assegnata a quella parola, e lì si somma 1. Parole uguali finiscono sempre nella stessa posizione.
# 4.	n è la lunghezza (norma) del vettore: la radice quadrata della somma dei quadrati dei suoi numeri.
# 5.	Se normalizza è vero e il vettore non è vuoto, ogni numero viene diviso per n: il vettore finale ha lunghezza 1.
# Il risultato è un vettore di lunghezza fissa (dim) quasi tutto fatto di zeri. È un modo semplice per ottenere vettori di dimensione costante da testi di lunghezza diversa (hashing trick).
# DOCUMENTI è un piccolo archivio di 4 testi (resi, rimborsi, spedizioni, pagamenti), con id, titolo e testo. 



import hashlib, math, re

def embedding_testo(testo, dim=1024, normalizza=True):
    v = [0.0] * dim
    for parola in re.findall(r"\w+", testo.lower()):
        numero = int(hashlib.md5(parola.encode("utf-8")).hexdigest(), 16)
        v[numero % dim] += 1.0
    n = math.sqrt(sum(x * x for x in v))
    if normalizza and n > 0:
        v = [x / n for x in v]
    return v

DOCUMENTI = [
    {"id": 0, "titolo": "Resi", "testo": "Il reso è gratuito entro quattordici giorni dalla consegna."},
    {"id": 1, "titolo": "Rimborsi", "testo": "Il rimborso arriva entro sette giorni dal ricevimento del reso."},
    {"id": 2, "titolo": "Spedizioni", "testo": "La spedizione costa cinque euro e la consegna avviene in tre giorni."},
    {"id": 3, "titolo": "Pagamenti", "testo": "Si accettano carta di credito e bonifico bancario."},
]
