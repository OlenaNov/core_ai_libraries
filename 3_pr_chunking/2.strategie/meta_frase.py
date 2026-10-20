
#Esercizio: chunk “a metà frase”
#Traccia. Taglia t = "Prima frase. Seconda frase. Terza frase." con chunk_fisso(t, 15) e conta i chunk che finiscono a metà frase, cioè che non terminano con un punto.

#Spiegazione.
#il testo è lungo 40 caratteri, quindi chunk_fisso(t, 15) usa le posizioni 0, 15, 30 e i pezzi sono t[0:15], t[15:30] e t[30:45] (che si ferma a 40).
#La riga sum(1 for p in pezzi if not p.endswith(".")) va letta così: per ogni chunk p che non finisce con un punto, produci un 1; sum li somma.



from chunk_fisso import *


t = "Prima frase. Seconda frase. Terza frase."

pezzi = chunk_fisso(t, 15)
a_meta = sum(1 for p in pezzi if not p.endswith("."))

print(pezzi)
print(a_meta, "chunk a metà frase")

