
# Costruisci indice: una lista con un dizionario
# per ogni frase di FRASI (id, testo, vettore)
# Per i vettori usa embedding_lista con compito="RETRIEVAL_DOCUMENT".
# Stampa quanti elementi ha, i campi del primo e la
# lunghezza del suo vettore

from typing import List, Dict, Any
from utils_ai_gemini import *
from exc_1 import vet

def costruisci_indice(testi: List[str], compito: str = "RETRIEVAL_DOCUMENT") -> List[Dict[str, Any]]:
    """
    Costruisce un indice vettoriale strutturato come lista di dizionari,
    associando a ciascuna frase il proprio ID, il testo e l'embedding.
    """
    vettori = embedding_lista(testi, compito=compito) 

    indice = [
        {
            "id": i,
            "testo": frase,
            "vettore": vettore 
        }
        for i, (frase, vettore) in enumerate(zip(testi, vettori))
    ]

    return indice

def main() -> None:
    COMPITO = "RETRIEVAL_DOCUMENT"

    print("⏳ Generazione degli embedding e costruzione dell'indice...")
    indice = costruisci_indice(FRASI, COMPITO)
    print("✅ Indice completato con successo!\n")

    print(f"📊 Numero totale di elementi nell'indice: {len(indice)}")

    for i in range(len(indice)):
        print(f"Elemento {indice[i]['id']}: {indice[i]['testo']} -> Vettore (primi 3 valori): {indice[i]['vettore'][:3]}")
        print(f"📐 Lunghezza del vettore: {len(indice[i]['vettore'])}\n")

if __name__ == "__main__":
    main()