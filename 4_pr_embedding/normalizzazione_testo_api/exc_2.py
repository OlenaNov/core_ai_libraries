

# Scrivi tokenizza(testo) e conta i token di ogni documento.
# Con Gemini: calcola l'embedding di ogni documento e 
# controlla la lunghezza dei vettori

from utils_ai import *

def tokenizza(testo):
    return normalizza_testo(testo).split()

print(tokenizza(DOCUMENTI[0]))
print([len(tokenizza(d)) for d in DOCUMENTI])
vettori = embedding_lista(DOCUMENTI)
print([len(v) for v in vettori])