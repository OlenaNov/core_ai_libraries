
#import math carica il modulo matematico. Serve math.sqrt (radice quadrata) per il coseno e math.log (logaritmo) per il TF-IDF.
# DOCUMENTI è una lista di 5 frasi brevi su un negozio online: resi, rimborsi, spedizioni, pagamenti, consegne. Sono il piccolo “archivio” su cui lavorano quasi tutti gli esercizi. Hanno maiuscole e punteggiatura apposta: il testo reale non è mai pulito. Nei dati le frasi si numerano da 0: DOCUMENTI[1] è "Il rimborso arriva entro sette giorni dal reso.".
# coseno(u, v) misura quanto due vettori sono simili, da 0 (nulla in comune) a 1 (stessa direzione). Passo per passo:
# 1.	zip(u, v) accoppia i numeri nella stessa posizione, e il ciclo ne somma i prodotti: il prodotto scalare num.
# 2.	nu e nv sono le lunghezze (norme) dei due vettori: la radice quadrata della somma dei quadrati dei loro numeri.
# 3.	Se uno dei vettori è fatto di soli zeri, la divisione sarebbe per zero: la funzione restituisce 0.
# 4.	Altrimenti restituisce num / (nu * nv).
# Il coseno ignora la lunghezza dei vettori e guarda solo la direzione, quindi si può confrontare testi di lunghezza diversa.


import math

DOCUMENTI = [
    "Il reso è gratuito entro quattordici giorni.",
    "Il rimborso arriva entro sette giorni dal reso.",
    "La spedizione costa cinque euro.",
    "Si accettano carta e bonifico.",
    "La consegna avviene in tre giorni.",
]

CORSO = [
    "Il corso è ideato per aspiranti programmatori python con l'intelligenza artificiale",
    "Il corso ha una durata di 240 ore",
    "Il numero dei partecipanti del corso è 18"
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

