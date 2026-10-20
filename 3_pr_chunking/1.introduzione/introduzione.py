
from preparazione_chunk import *

def chunk(testo, dim, overlap):
    passo = dim - overlap
    # for i in range(0, len(testo), passo):
    #     print(f"passo = {passo}")
    #     print(f"len = {len(testo)}")
    #     print(i, i + dim)
    return [testo[i:i + dim] for i in range(0, len(testo), passo)]

print(chunk(testo, 8, 0))
print(chunk(testo, 8, 3))
print(chunk(testo, 4, 0))