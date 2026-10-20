from math import ceil
from typing import Dict

def calculate_chunk_metrics(text: str, step: int) -> Dict[str, int]:
    """
    Calcola le metriche strutturali di un testo, inclusi caratteri, parole 
    e stima dei token tematici basata sul passo di chunking.

    Args:
        text: La stringa di testo da analizzare.
        step: Il passo (step) utilizzato per la suddivisione in chunk. Deve essere > 0.

    Returns:
        Un dizionario contenente le metriche calcolate:
            - characters: numero totale di caratteri.
            - words: numero totale di parole.
            - thematic_tokens: numero stimato di chunk/token tematici.

    Raises:
        TypeError: Se 'text' non è una stringa.
        ValueError: Se 'step' è minore o uguale a zero.
    """
    if not isinstance(text, str):
        raise TypeError("Il parametro 'text' deve essere una stringa.")

    if step <= 0:
        raise ValueError("Il parametro 'step' deve essere un intero maggiore di zero.")

    if not text.strip():
        return {
            "characters": 0,
            "words": 0,
            "thematic_tokens": 0
        }
    
    return {
        "characters": len(text),
        "words": len(text.split()),
        "thematic_tokens": ceil(len(text) / step)
    }
