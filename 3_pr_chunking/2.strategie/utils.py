import math
from collections import Counter

# Spiegazione

#dividi_frasi

#Riceve un testo e restituisce la lista delle sue frasi, 
# ciascuna intera e con il punto finale.
#frasi = [] crea una lista vuota in cui raccogliere le frasi.
#testo.split(".") taglia il testo a ogni punto (il punto sparisce) e dà una lista di pezzi.
#for pezzo in ... prende i pezzi uno alla volta.
#if pezzo.strip(): controlla che il pezzo contenga del testo. strip() toglie gli spazi ai bordi, e una stringa vuota in un if conta come falsa.

#tok_parole

#Divide il testo a ogni spazio e restituisce le parole: è il tokenizzatore più semplice, un token per parola. 
# Per esempio "La PEC ha valore legale." → ['La', 'PEC', 'ha', 'valore', 'legale.'].
# La punteggiatura resta attaccata alla parola (legale.), 
# a differenza di un tokenizzatore reale.

#tok_sottoparole

#Simula un tokenizzatore a sottoparole: taglia ogni parola in pezzi di al massimo n caratteri (per default 4).
#token = [] lista vuota per i pezzi.
#for parola in testo.split(): scorre le parole.
#range(0, len(parola), n) genera le posizioni di partenza dei pezzi: 0, n, 2n... fino alla fine della parola.
#parola[k:k + n] taglia il pezzo. Se la parola finisce prima, Python restituisce solo ciò che c’è.
#Per elettronica (11 caratteri), range(0, 11, 4) dà 0, 4, 8, quindi i pezzi sono elet, tron, ica.



def dividi_frasi(testo):
    frasi = []
    for pezzo in testo.split("."):
        if pezzo.strip():
            frasi.append(pezzo.strip() + ".")
    return frasi

def tok_parole(testo):
    # un token per parola (la punteggiatura resta attaccata alla parola)
    return testo.split()

def tok_sottoparole(testo, n=4):
    # simula le sottoparole: pezzi di al massimo n caratteri
    token = []
    for parola in testo.split():
        for k in range(0, len(parola), n):
            token.append(parola[k:k + n])
    return token