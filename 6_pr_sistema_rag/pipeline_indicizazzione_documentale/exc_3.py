
# Traccia. Leggi i due file stampando il testo o l’errore. 
# Poi guarda i byte grezzi di latin.txt e prova a decodificarli 
# come Latin-1.

from initial import *

for nome in ('utf8.txt', 'latin.txt'):
    percorso = cartella2/nome
    try:
        testo = leggi_testo(percorso)
        print(nome,"->",repr(testo),len(testo))
    except ValueError as errore:
        print(nome,"-> errore:",errore)
byte = (cartella2/"latin.txt").read_bytes()
print(byte)
print(byte.decode("latin-1"))