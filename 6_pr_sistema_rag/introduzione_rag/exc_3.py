# Traccia. Stampa quanti documenti ci sono, il totale delle parole, 
# l’elenco ordinato delle fonti e il documento più lungo con la 
# sua lunghezza.

from initial import *

print(len(DOCUMENTI))

totale_parole = 0
for d in DOCUMENTI:
    totale_parole += len(d["testo"].split())
print(totale_parole)

print(sorted(d["fonte"] for d in DOCUMENTI))

doc_lungo = max(DOCUMENTI, key=lambda d: len(d["testo"]))
print(doc_lungo["fonte"], len(doc_lungo["testo"]))