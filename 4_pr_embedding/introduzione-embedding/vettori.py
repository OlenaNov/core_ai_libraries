from utils import *

#Traccia. Un modello assegna a ogni parola un vettore. 
# Qui usiamo vettori a 2 numeri, inventati per l’esercizio: gatto = [0.9, 0.1], 
# cane = [0.85, 0.2], mela = [0.1, 0.9]. 
# Stampa la dimensione del vettore di gatto e controlla la dimensione di tutti i vettori.

#SPIEGAZIONE

#parole è un dizionario: ogni chiave (la parola) è associata a un valore (il vettore, cioè una lista di due numeri).
#parole["gatto"] legge il vettore associato a gatto, e len(...) ne conta gli elementi: 2. Questa è la dimensione del vettore.
#parole.values() dà tutti i vettori, e la list comprehension [len(v) for v in ...] costruisce la lista delle loro lunghezze: 2, 2, 2.


parole = {
    "gatto": [0.9, 0.1],
    "cane": [0.85, 0.2],
    "mela": [0.1, 0.9],
}
print(len(parole["gatto"]))
print([len(v) for v in parole.values()])
