#Traccia: crea il file poesia.txt con tre righe, 
# poi leggilo e stampa ogni riga preceduta dal suo numero (1 : ..., 2 : ...).

from pathlib import Path

cartella = Path(__file__).parent
percorso = cartella / "poesia.txt"

percorso.write_text("Prima riga\nSeconda riga\nTerza riga", encoding="utf-8")

testo = percorso.read_text(encoding="utf-8")

numero = 1
for riga in testo.splitlines():
    print(numero, ":", riga)
    numero = numero + 1
