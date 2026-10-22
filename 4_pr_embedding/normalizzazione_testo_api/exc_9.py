
# Scrivi tf(testo, indici) e verifica che la somma sia 1 per DOCUMENTI[1].
#Con Gemini: raddopia il documento (d+" "+d) e confronta il coseno
# tra il documento e la sua versione raddopiata con il 
# TF e con l'embedding

from utils_ai import *

def tf(testo, indici):
    c = vettore_conteggio(testo, indici)
    n = sum(c)
    return [x/n for x in c]

doc = DOCUMENTI[1]
t = tf(doc, indici)
print("Somma TF:", round(sum(t), 2))
print("Parole presenti:", [(p, round(x, 3)) for p, x in zip(vocabolario, t) if x])


doppio = doc + " " + doc


print("Coseno TF:", round(coseno(tf(doc, indici), tf(doppio, indici)), 2))

g1, g2 = embedding_lista([doc, doppio])

print("Coseno Embedding Gemini:", round(coseno(g1, g2), 2))