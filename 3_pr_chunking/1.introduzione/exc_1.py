# !!TODO 

import math
from utils import *
from chunk_with_overlap import *

def n_attesi(lunghezza, dim, overlap=0):
    step = dim - overlap
    if step <= 0:
        return 0
    return math.ceil(lunghezza / step)

for dim, ov in [(100, 0), (100, 20), (50, 10)]:
    print(dim, ov, n_attesi(len(TEXT), dim, ov), len(chunk_characters(TEXT, dim, ov)))