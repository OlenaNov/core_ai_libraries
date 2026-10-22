# Il vettore a conteggio di un documento
# Scrivi vettore conteggio(testo, indici) e calcolalo per DOCUMENTI[1]
# e per "reso reso reso gratuito"
# Con Gemini: confronta il vettore a conteggio di DOCUMENTI[1] con il
# suo embedding: quanti numeri ha, quanti sono diversi da zero?

from utils_ai import *

def vettore_conteggio(testo, indici):
    v = [0] * len(indici)

    for t in tokenizza(testo):
        if t in indici:
            v[indici[t]] += 1

    return v

v = vettore_conteggio(DOCUMENTI[1], indici)
print(v)
print(sum(v))
print([(p, c) for p, c, in zip(vocabolario, v) if c])

v2 = vettore_conteggio("reso reso reso gratuito", indici)
print([(p, c) for p, c, in zip(vocabolario, v2) if c])

vg = embedding_lista(DOCUMENTI[1])
print(len(v), sum(1 for x in v if x!=0))
print(len(vg), sum(1 for x in vg if x!=0))
