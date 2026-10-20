#Esercizio: la sovrapposizione

#Traccia. Usa la funzione dell’esercizio 2 con dim=10 e overlap=4. 
# Quanti chunk ottieni e qual è il passo?

#Spiegazione.
#Che cosa cambia: con overlap=4 il passo diventa 10 - 4 = 6. 
# I chunk avanzano di 6 lettere ma ne contengono 10, quindi si sovrappongono di 4.

from chunk_fisso import *


print(chunk_fisso(alfabeto, 10, 4))
print("passo =", 10 - 4)

