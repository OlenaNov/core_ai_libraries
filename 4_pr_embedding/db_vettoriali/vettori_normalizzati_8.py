# Esercizio 8: con vettori normalizzati le tre misure coincidono
# Traccia. Normalizza la domanda [0.9, 0.1, 0.0] e tutti i vettori dell’archivio. 
# Ordina gli id dal più vicino al più lontano con tre misure: coseno (decrescente), prodotto scalare (decrescente), distanza (crescente).
# Verifica che i tre ordinamenti coincidano. Poi controlla, per i record 1 e 2, che il quadrato della distanza sia uguale a 2 - 2 × coseno.

from preparazione_1 import *
from intro_db_vettoriali import *
from prodotto_scalare_7 import *
from norma_mormalizzazione_6 import *

qn = normalizza([0.9, 0.1, 0.0])
vn = {i: normalizza(r["vettore"]) for i, r in db.items()}

per_coseno = sorted(vn, key=lambda i: -coseno(qn, vn[i]))
per_prodotto = sorted(vn, key=lambda i: prodotto_scalare(qn, vn[i]))
per_distanza = sorted(vn, key=lambda i: distanza(qn, vn[i]))

print(per_coseno, per_prodotto, per_distanza)
print(per_coseno == per_prodotto == per_distanza)

u, v = vn[1], vn[2]
print(round(distanza(u, v) ** 2), 4, round(2-2*coseno(u, v), 4))