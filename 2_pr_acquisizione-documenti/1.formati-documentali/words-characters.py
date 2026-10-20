#Traccia: leggi nota.txt (creato nell'esercizio 2) e stampa quanti caratteri e quante parole contiene.

from pathlib import Path

cartella = Path(__file__).parent
percorso = cartella / "write-python.txt"

testo = percorso.read_text(encoding="utf-8")

print("Caratteri:", len(testo))
print("Parole:", len(testo.split()))
