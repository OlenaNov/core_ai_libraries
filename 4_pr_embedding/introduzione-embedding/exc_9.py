# Traccia. Costruisci indice: una lista con un dizionario per 
# ogni frase, che contiene l’identificativo, il testo e il 
# vettore. Stampa quanti elementi ha, quali campi ha il 
# primo e quanto è lungo il suo vettore

from utils import FRASI
from exc_6 import vocabolario
from exc_6 import embedding

indice = [{"id": i, "testo": f, "vettore": embedding(f, vocabolario)} for i, f in enumerate(FRASI)]

print(len(indice))
print(list(indice[0].keys()))
print(len(indice[0]["vettore"]))