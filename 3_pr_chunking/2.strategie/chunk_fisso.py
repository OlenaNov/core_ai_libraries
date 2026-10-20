#Esercizio: chunk a lunghezza fissa

#Traccia. Scrivi chunk_fisso(testo, dim, overlap=0) che taglia il testo a intervalli regolari. 
# Provala su "abcdefghijklmnopqrstuvwxyz" con dim=10.

#Spiegazione.

	#def chunk_fisso(testo, dim, overlap=0): tre parametri, di cui overlap 
    # ha un valore predefinito di 0. Si può scrivere chunk_fisso(t, 10) e l’overlap vale 0.
	#passo = dim - overlap: di quanto avanza l’inizio di ogni chunk. Senza overlap il passo è uguale alla dimensione.
	#range(0, len(testo), passo): genera le posizioni di partenza: 0, passo, 2·passo...
	#testo[i:i + dim]: il pezzo che parte da i ed è lungo dim.
	#if testo[i:i + dim].strip(): tiene il pezzo solo se contiene qualcosa oltre agli spazi, per evitare chunk vuoti.


def chunk_fisso(testo, dim, overlap=0):
    passo = dim - overlap
    return [testo[i:i + dim] for i in range(0, len(testo), passo)
            if testo[i:i + dim].strip()]

alfabeto = "abcdefghijklmnopqrstuvwxyz"
print(chunk_fisso(alfabeto, 10))

