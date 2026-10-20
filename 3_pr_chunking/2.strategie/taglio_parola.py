
#Esercizio taglio sul confine di parola

#Traccia. Scrivi chunk_parole(testo, dim) che non taglia mai in mezzo a una parola: se il taglio cade dentro una parola,
# arretra fino allo spazio precedente. Provala sul testo dell’esercizio 1 con dim=20.

#Spiegazione.
#invece di tagliare esattamente dopo dim caratteri, 
# si taglia sull’ultimo spazio disponibile prima di quel punto, 
# così nessuna parola viene spezzata. dim diventa un limite massimo.


from lunghezza_fissa import *


def chunk_parole(testo, dim):
    chunk, inizio = [], 0

    while inizio < len(testo):
        fine = min(inizio + dim, len(testo))

        if fine < len(testo):
            taglio = testo.rfind(" ", inizio, fine)

            if taglio > inizio:
                fine = taglio

        chunk.append(testo[inizio:fine].strip())
        inizio = fine
        
    return chunk

print(chunk_parole(testo, 20))

