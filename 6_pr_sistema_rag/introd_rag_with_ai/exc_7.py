# Traccia. Scrivi costruisci_contesto(risultati) che trasforma i 
# chunk recuperati in un testo numerato [1] ... (fonte: ...), e 
# restituisce "(nessun documento trovato)" se non c’è nulla. 
# Provala con i 2 chunk migliori per "Entro quanti giorni arriva il
#  rimborso?" e con una lista vuota.

from initial import *

def costruisci_contesto(risultati):
    if not risultati:
        return "(Nessun documento trovato)"
    righe = []
    for numero, (pnteggio, chunk) in enumerate(risultati, start=1):
        righe.append(f"[{numero}]{chunk["testo"]}(fonte:{chunk["fonte"]})")
    return "\n".join(righe)

risultati = cerca("Entro quanti giorni arriva il rimborso?", indice, 2)
print(costruisci_contesto(risultati))
print("----")
print(costruisci_contesto([]))