
from collections import Counter
from utils import *
from exc_1 import *

tutti = []

for doc in CORSO:
    tutti += tokenizza(doc)

vocabolario = sorted(set(tutti))

indice = {
    parola: posizione for parola, posizione in enumerate(vocabolario)
}

print(vocabolario, len(vocabolario))
print(vocabolario.index("corso"))
print(vocabolario.index("programmatori"))
print(vocabolario.index("intelligenza"))