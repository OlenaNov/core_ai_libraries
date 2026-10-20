# TODO !!!!!!!!!!!!!!!!

from typing import TypeVar, List, Sequence

T = TypeVar("T")

def parameter_validation(data: Sequence[T], size: int, overlap: int) -> List[str, int]:
        if size <= 0:
            raise ValueError("La dimensione del chunk (size) deve essere maggiore di 0.")
            return False
        
        if overlap >= size:
            raise ValueError("L'overlap deve essere strettamente inferiore alla dimensione del chunk (size).")
            return False
        
        if not data:
            return False

        return True
def chunk_characters(data: Sequence[T], size: int, overlap: int) ->List[str]:
    """
    Suddivide una sequenza in chunk sovrapposti di dimensione definita.

    Args:
        data: La sequenza di input (es. stringa, lista, tupla) da suddividere.
        size: La dimensione fissa di ciascun chunk.
        overlap: Il numero di elementi condivisi tra chunk consecutivi.

    Returns:
        Una lista contenente i chunk risultanti.

    Raises:
        ValueError: Se la dimensione del chunk è <= 0 o se l'overlap è maggiore/uguale alla dimensione.
    """

    step = size - overlap

    return [data[i:i + size] for i in range(0, len(data), step)]


def chunk_words(data: Sequence[T], size: int, overlap: int) -> List:
    if not parameter_validation(data, size, overlap):
         print("Date is not valid")
    
    step = size - overlap
    words = data.split()

    return [data[i:i + size] for i in range(0, len(words), step)]


chunk_words("mgbklv fdskjbdf kvdopfjbd goerpjgpor kopfwesjgporej fdhsrg rehrthw54tr rehrt greh", 3, 1)