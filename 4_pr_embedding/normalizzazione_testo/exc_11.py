# Scrivi tf(testo, indici) che restituisce, per ogni parola 
# la sua frequenza relativa: il conteggio diviso per il numero totale 
# di token. Calcola per DOCUMENTI[1] e verifica che la somma sia 1.

from utils import *
from exc_8 import vettore_conteggio
from exc_5 import indice, vocabolario

def tf(testo, indici):
    c = vettore_conteggio(testo, indici)
    n = sum(c)
    return [x / n for x in c]

t = tf(DOCUMENTI[1], indice)

print("Vettore TF (frequenze relative):")
print(t)

print("Somma delle frequenze:", round(sum(t), 2))

print("\nParole presenti in DOCUMENTI[1] e i rispettivi TF:")
print([(p, round(x, 3)) for p, x in zip(vocabolario, t) if x])
