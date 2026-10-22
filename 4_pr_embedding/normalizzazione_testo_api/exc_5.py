# Scrivi one_hot(parola, indice), calcola quello di reso rìe il coseno tra reso e rimborso
# Con Gemini calcola il coseno tra gli embedding di reso e rimborso e tra reso e bonifico

from utils_ai import *

def one_hot(parola, indici):
    vettore = [0] * len(indici)
    vettore[indici[parola]] = 1
    return vettore

uno = one_hot("reso", indici)
print(indici)
print(uno)
print(sum(uno), uno.index(1))

due = one_hot("rimborso", indici)
print(coseno(uno, due))
print(coseno(uno, uno))

emb_parole = dict(
    zip(vocabolario, embedding_lista(vocabolario))
)

print(coseno(emb_parole["reso"], emb_parole["rimborso"]))
print(coseno(emb_parole["reso"], emb_parole["bonifico"]))