#Traccia: crea il file nota.txt con scritto Oggi studio Python.,
# poi rileggilo e stampane il contenuto.
from pathlib import Path

cartella = Path(__file__).parent
percorso = cartella / "write-python.txt"

percorso.write_text("Oggi studio Python.", encoding="utf-8")

testo = percorso.read_text(encoding="utf-8")
print(testo)
