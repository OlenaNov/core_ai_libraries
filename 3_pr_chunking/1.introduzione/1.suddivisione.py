#Scrivi misure(testo) che restituisce un dizionario con numero di caratteri,
# di parole e di token stimati (1 token ≈ 4 caratteri). Provala su TESTO.

#Spiegazione: il carattere è la misura più semplice, 
# la parola è quella che percepisce chi scrive, 
# il token è l’unità con cui i modelli leggono davvero e da cui dipendono limiti e costi. 
# La stima con 4 caratteri per token è solo un ordine di grandezza: il numero esatto dipende dal tokenizzatore del modello.

from utils import *

def misure(testo):
    return {
        "caratteri": len(testo),
        "parole": len(testo.split()),
        "token_stimati": round(len(testo) / 4),
    }
