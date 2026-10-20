
# Controlla che FRASI e vet abbiano le stessa lunghezza. 
# Poi costruisci un dizionario catalogo che associa ogni frase
# ai primi 3 numeri del suo vettore e stampalo.

from utils_ai_gemini import *
from exc_1 import vet

print(len(FRASI))
print(len(vet))
print(len(FRASI) == len(vet))

catalogo = {}

for frase, v in zip(FRASI, vet):
    catalogo["frase"] = [round(x, 3) for x in v[:3]]
    for frase, inizio in catalogo.items():
        print(frase, "->", inizio)