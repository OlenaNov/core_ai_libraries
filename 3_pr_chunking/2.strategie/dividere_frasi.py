
#Esercizio: dividere in frasi

#Traccia. Con dividi_frasi, ricava la lista delle frasi di questo testo:

#"La PEC ha valore legale. La fattura va inviata. Il consumatore può recedere."

# Spiegazione
# per verificare il comportamento di dividi_frasi guarda il file utils.py

from utils import *

t = "La PEC ha valore legale. La fattura va inviata. Il consumatore può recedere."
frasi = dividi_frasi(t)
print(len(frasi))
print(frasi)

