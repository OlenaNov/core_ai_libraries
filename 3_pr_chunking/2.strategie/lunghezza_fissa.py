# Esercizio: misurare un testo
#Traccia. Dato testo = "La posta elettronica certificata ha valore legale.", stampa il numero di caratteri e di parole.

#Spiegazione.
	#len(testo) conta tutti i caratteri, compresi i 6 spazi e il punto finale: 50.
	#testo.split() senza argomenti divide a ogni spazio e restituisce la lista ['La', 'posta', 'elettronica', 'certificata', 'ha', 'valore', 'legale.']. len() di questa lista conta 7 elementi.
	#print con più valori separati da virgola li stampa uno dopo l’altro, separati da uno spazio. Le stringhe "car." e "parole" fanno da etichette.


testo = "La posta elettronica certificata ha valore legale."
print(len(testo), "car.", len(testo.split()), "parole")

