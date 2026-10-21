# Scrivi tokenizza(testo)che normalizza il testo e lo divide in parole
# (token). 
import math
from utils import *
from norma_testo import *

def tokenizza(testo):
    return normalizza_testo(testo).split()

print(tokenizza(DOCUMENTI[0]))
print([len(tokenizza(t)) for t in DOCUMENTI])