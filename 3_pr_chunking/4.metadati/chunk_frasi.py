
#Scrivi chunk_frasi(testo, max_car) che aggiunge frasi intere a un chunk finché non supererebbe max_car caratteri.
# Provala con max_car=200.
#Spiegazione: la variabile corrente contiene il chunk in costruzione.
# Per ogni frase si controlla se aggiungerla (più 1 per lo spazio) supererebbe il limite: in quel caso 
# si chiude il chunk e si riparte dalla frase;
# altrimenti la si accoda. Dopo il ciclo va salvato anche l’ultimo chunk. 
# Nessuna frase viene spezzata, ma le lunghezze sono irregolari (186 e 153).

from utils import *
from exc_4 import *

def chunk_frasi(testo, max_car):
    chunk, corrente = [], ""

    for frase in dividi_frasi(testo):
        if corrente and len(corrente) + 1 + len(frase) > max_car:
            chunk.append(corrente)
            corrente = frase
        else:
            corrente = (corrente + " " + frase).strip()

    if corrente:
        chunk.append(corrente)
        
    return chunk 

c = chunk_frasi(test, 200)
print(len(c), [len(x) for x in c])
for x in c:
    print(repr(x))