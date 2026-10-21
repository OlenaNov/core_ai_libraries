
from collections import Counter
from utils import *
from exc_1 import tokenizza

tutti = []

for x in CORSO:
    tutti += tokenizza(x)

print(len(tutti))
print(len(tutti), len(set(tutti)))
print(Counter(tutti).most_common(5))