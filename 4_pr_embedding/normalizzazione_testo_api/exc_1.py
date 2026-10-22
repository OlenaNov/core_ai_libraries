
# Scrivi normalizza_testo(testo)
# (minuscolo, niente punteggiatura, niente spazi e bordi)
# e provala su DOCUMENTI[1]
# su " Reso GRATUITO!!! Entro 14 giorni, sempre." 
# e su "L'uomo è qui."
# Con Gemini: calcola l'embedding del testo "sporco"
# e di quello normalizzato e confronta i due con il coseno

from utils_ai import *

def normalizza_testo(testo):
    pulito=""

    for c in testo.lower():

        if c.isalnum() or c == " ":
            pulito += c

    return pulito.strip()

def main():
    ts = " Reso GRATUITO!!! Entro 14 giorni, sempre."

    print(normalizza_testo(DOCUMENTI[1]))
    print(normalizza_testo(ts))
    print(normalizza_testo("L'uomo è qui."))

    v1 = embedding_lista([ts, normalizza_testo(ts)])
    print(round(coseno(v1[0], v1[1]), 2))

    v2 = embedding_lista([DOCUMENTI[1], normalizza_testo(DOCUMENTI[1])])
    print(round(coseno(v2[0], v2[1]), 2))
    

if __name__ == "__main__":
    main()