
from utils import *
from norma_testo import *

def tokenizza(testo):
    return normalizza_testo(testo).split()

print(list(tokenizza(i) for i in CORSO))
print([len(tokenizza(t)) for t in CORSO])