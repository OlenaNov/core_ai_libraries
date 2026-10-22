# Il vettore di un doccumento ha quasi tutti zeri. Trasforma M[1] in un dizionario 
# che conserva solo le posizioni diverse da zero, confronta quanti 
# elementi contiene con la dimensione del vettore, e verifica di poter 
# ricostruire il vettore completo

from utils import *
from exc_5 import indice, vocabolario, DOCUMENTI
from exc_8 import vettore_conteggio


documento_termine = [vettore_conteggio(doc, indice) for doc in DOCUMENTI]

def trasf(vettore):
    return {
        i: c for i, c in enumerate(vettore) if c
    }


temp = trasf(documento_termine[1])
x = [0] * len(documento_termine[1])

for i, c in temp.items():
    x[i] = c

print("Dizionario sparso per documento_termine[1]:")
print(temp)

print("Elementi non zero:", len(temp), "| Dimensione totale del vettore:", len(documento_termine[1]))
print("I vettori coincidono?", x == documento_termine[1])