# TODO !!!!

import math
from typing import List, Dict, Set, Tuple

# ==========================================
# 1. CORPUS DI PARTENZA E CONFIGURAZIONE
# ==========================================

FRASI: List[str] = [
    "Il gatto dorme sul divano",
    "Il cane corre nel parco",
    "La mela è un frutto dolce",
    "Il gatto mangia la mela",
    "Un cane abbaia forte nel giardino"
]

STOP_WORDS: Set[str] = {"il", "la", "un", "una", "è", "sul", "nel"}

# ==========================================
# 2. FUNZIONI DI ELABORAZIONE TESTUALE
# ==========================================

def crea_vocobolario(corpus: List[str], stop_words: Set[str]) -> List[str]:
    """
    Estrae le parole uniche dal corpus, rimovendo le stop words,
    e restituisce una lista ordinata alfabeticamente.
    """

    parole_uniche = {
        parola 
        for frase in corpus 
        for parola in frase.lower().split()
        if parola not in stop_words
        }
    return sorted(list(parole_uniche))

def calcola_embedding(frase: str, vocabolario: List[str], stop_words: Set[str]) -> List[int]:
    """
    Converte una frase in un vettore di frequenze (Bag-of-Words)
    basato esclusivamente sulle parole presenti nel vocabolario
    """

    parole_frase = [p for p in frase.lower().split() if p not in stop_words]
    return [parole_frase.count(parola) for parola in vocabolario]

# ==========================================
# 3. MATEMATICA DEI VETTORI (Similitudine)
# ==========================================

def prodotto_scalare(u: List[float], v:List[float]) -> float:
    """Calcola il dot product tra due vettori."""
    return sum(a * b for a, b in zip(u, v))

def norma(v: List[float]) -> float:
    """Calcola la norma (lunghezza euclidea) di un vettore"""
    return math.sqrt(sum(x * x for x in v))

def similarità_coseno(u: List[float], v: List[float]) -> float:
    """
    Calcola la similarità del coseno tra due vettori.
    Restituisce un valore tra -1 e 1 (1 = identici, 0 = ortogonali).
    """

    denominatore = norma(u) * norma(v)
    if denominatore == 0.0:
        return 0.0
    return prodotto_scalare(u, v) / denominatore

# ==========================================
# 4. ESECUZIONE DELLA PIPELINE (Main)
# ==========================================

def main() -> None:
    print("--- 1. GENERAZIONE VOCABOLARIO ---")
    vocabolario = crea_vocobolario(FRASI, STOP_WORDS)
    print(f"Vocabolario pulito ({len(vocabolario)} parole):")
    print(f"{vocabolario}\n")

    print("--- 2. CREAZIONE DELL'INDICE VETTORIALE ---")
    # Costruiamo una lista di dizionari (l'indice) che collega ID, Testo e Vettore
    indice: List[Dict] = [
        {
            "id": i,
            "testo": frase,
            "vettore": calcola_embedding(frase, vocabolario, STOP_WORDS)
        }
        for i, frase in enumerate(FRASI)
    ]

    for item in indice:
        print(f"ID {item['id']} | Testo: '{item['testo']}' | Vettore: {item['vettore']}\n")

    print("--- 3. TEST DI RICERCA SEMANTICA (Similarità del Coseno) ---")

    v0 = indice[0]["vettore"]
    v1 = indice[1]["vettore"]
    v3 = indice[3]["vettore"]

    sim_0_1 = similarità_coseno(v0, v1)
    sim_0_3 = similarità_coseno(v0, v3)

    print(f"Confronto: '{indice[0]['testo']}' <-> '{indice[1]['testo']}'")
    print(f"Similarità: {sim_0_1:.2f}\n")

    print(f"Confronto: '{indice[0]['testo']}' <-> '{indice[3]['testo']}'")
    print(f"Similarità: {sim_0_3:.2f}")

if __name__=="__main__":
    main()