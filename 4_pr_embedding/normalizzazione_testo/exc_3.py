# Metti in una sola lista i token di tutti i documenti.
# Quanti token ci sono in totale e quante sono le parole diverse
# quali sono le più frequenti

from collections import Counter

from utils import *
from exc_2 import tokenizza

tutti = []

for x in DOCUMENTI:
    tutti += tokenizza(x)

print(len(tutti), len(set(tutti)))
print(Counter(tutti).most_common(5)) # 5 parole più frequenti