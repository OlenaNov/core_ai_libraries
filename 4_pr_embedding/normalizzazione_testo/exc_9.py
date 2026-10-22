
# A partire dal vettore v2 dell'esercizio precedente("reso reso reso gratuito"),
# costruisci il vettore binario: 1 se la parola è presente, 
# 0 se è assente, senza contare  le ripetizioni


from utils import *
from exc_5 import *
from exc_8 import *

b = [1 if c > 0 else 0 for c in v2]
print([(p, c) for p, c in zip(vocabolario, b) if c])
print(sum(b))

