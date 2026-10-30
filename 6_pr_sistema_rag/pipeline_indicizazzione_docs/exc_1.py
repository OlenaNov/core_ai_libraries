# Traccia. Scrivi la pipeline come lista di fasi (nome e funzione)
#  e applicala a un testo, stampando a ogni passaggio il tipo e 
# la lunghezza del risultato.

from initial import *


fasi = [
    ("normalizzazione", normalizza),
    ("chunking", dividi),
    ("embedding", vettorizza)
]
dato = "Il reso è gratuito.\n|| prodotto deve essere integro."

print("Ingresso".ljust(16), type(dato).__name__, len(dato))
for nome, funzione in fasi:
    dato = funzione(dato)
    print(len(dato[0]), sum(1 for x in dato [0] if x))