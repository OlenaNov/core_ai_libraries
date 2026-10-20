# Traccia. Confronta la frase 0 (il gatto dorme sul divano) con 
# la frase 4 (il cane corre nel parco) usando l’embedding a 
# conteggio. Poi ripeti dopo aver tolto le parole troppo 
# comuni (il, la, un, una, è, sul, nel).

import math
from utils import FRASI
from exc_5 import vocabolario

STOP = {"il", "la", "un", "una", "è", "sul", "nel"}

def embedding_pulito(frase, vocabolario):
    parole = [p for p in frase.lower().split() if p not in STOP]
    return [parole.count(p) for p in vocabolario]

print([p for p, c in zip(vocabolario, embedding_pulito(FRASI[0], vocabolario)) if c])