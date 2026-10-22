
# A partire da "reso reso reso gratuito" costruisci il
#  vettore binario (1 se presente, 0 se assente)
# Con Gemini: confronta "reso reso reso gratuito" e 
# "reso gratuito" con il coseno usando i conteggi, 
# il vettore binario e l'embedding

from utils_ai import *

b = [1 if c>0 else 0 for c in v2]
print(sum(b))

a_txt = "reso reso reso gratuito"
b_txt = "reso gratuito"

ca = vettore_conteggio(a_txt, indici)
cb = vettore_conteggio(b_txt, indici)
ba = [1 if c>0 else 0 for c in ca]
bb = [1 if  c>0 else 0 for c in cb]
print(round(coseno(ca, ba), 2))
print(round(coseno(ba, bb), 2))

ga, gb = embedding_lista([a_txt, b_txt])
print(round(coseno(ga, gb)), 2)

