
# Metti in una lista i token di tutti i documenti
# quanti sono in totale, quante le parole diverse,
# quali le più frequenti? 
# Con Gemini: calcolare l'embedding di ognuna delle
# parole diversee trova le 3 più vicine a reso

from collections import Counter
from utils_ai import *
from exc_2 import tokenizza, normalizza_testo

tutti = []
for d in DOCUMENTI:
    tutti += tokenizza(d)

print(f"Totale {len(tutti)}, {len(set(tutti))}")
print(Counter(tutti).most_common(10))

parole = sorted(set(tutti))
vp = embedding_lista(parole)
pp = parole.index("reso")

vicine = sorted(
    ((coseno(vp[pp], v), p) for p, v in zip(parole, vp) if p != "reso"),
    reverse=True
)

print([(p, round(s, 2)) for s, p in vicine[:3]])