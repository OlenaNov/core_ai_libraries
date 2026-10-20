#Scrivi n_attesi(lunghezza, dim, overlap) che calcola con una formula quanti chunk si ottengono,
# e verifica che coincida con chunk_caratteri per tre combinazioni di parametri.
#Spiegazione: i chunk partono ogni passo caratteri,
# quindi il loro numero è lunghezza / passo arrotondato per eccesso (math.ceil).
# Con 340 caratteri e passo 80 si ha 340 / 80 = 4,25, quindi 5 chunk.
# Saper prevedere il numero di chunk serve a stimare in anticipo costi e dimensione dell’indice.

from utils import *
from chunk_with_overlap import *

def n_attesi(lunghezza, dim, overlap=0):
    return math.ceil(lunghezza / (dim - overlap))

for dim, ov in [(100, 0), (100, 20), (50, 10)]:
    # print(dim, ov, n_attesi(len(test), dim, ov), len(chunk_caratteri(test, dim, ov)))
    print(dim, ov, n_attesi(len(ordine), dim, ov))