
#Traccia. Scrivi normalizza_testo(testo) che porta il testo in minuscolo, 
# elimina la punteggiatura e toglie gli spazi ai bordi. Provala su DOCUMENTI[1], 
# su " Reso GRATUITO!!! Entro 14 giorni, sempre. " e su "L'uomo è qui.".

#SPIEGAZIONE

#Il codice, riga per riga:
#testo.lower() porta tutto in minuscolo, così Reso, RESO e reso diventano la stessa parola.
#pulito = "" parte da una stringa vuota in cui si accumulano i caratteri tenuti.
#for c in ...: scorre il testo un carattere alla volta.
#c.isalnum() è vero per lettere e cifre (comprese le lettere accentate come è). c == " " tiene gli spazi. Tutto il resto (punti, virgole, punti esclamativi, apostrofi) viene scartato.
#pulito.strip() toglie gli spazi in testa e in coda.
#Cosa succede. In DOCUMENTI[1] il punto finale scompare e Il diventa il. Nel secondo testo spariscono i !!! e la virgola e gli spazi ai bordi, e GRATUITO diventa gratuito.
#Un limite. L’apostrofo viene eliminato e incolla le due parole: L'uomo diventa luomo. È un effetto collaterale di una pulizia così semplice; un sistema reale gestisce l’apostrofo a parte.
#Da ricordare. Prima di trasformare un testo in numeri lo si normalizza, altrimenti Reso e reso verrebbero contati come parole diverse. Le regole di normalizzazione si decidono una volta e vanno applicate sia ai documenti sia alle domande.

from utils import *

def normalizza_testo(testo):
    pulito = ""
    for c in testo.lower():
        if c == "'":
            c = " "
        if c.isalnum() or c == " ":
            pulito += c
    return pulito.strip()

print(normalizza_testo(DOCUMENTI[1]))
print(normalizza_testo("  Reso GRATUITO!!! Entro 14 giorni, sempre.  "))
print(normalizza_testo("L'uomo è qui."))

