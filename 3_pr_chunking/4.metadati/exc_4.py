
from utils import *
import re

def dividi_frasi(testo):
    pezzi = re.split(r"(?<=[.!?])\s+(?=[A-Z])", testo)
    return [f.strip() for f in pezzi if f.strip()]

# frasi = dividi_frasi(testo)
#print(len(frasi), [len(f) for f in frasi])
print(dividi_frasi("Il sig. Rossi ha pagato 1.234,50 euro. Ha ricevuto il rimborso"))