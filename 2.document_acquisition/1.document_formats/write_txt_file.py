
from pathlib import Path

cartella = Path(__file__).parent

percorso = cartella / "write_file.txt"

percorso.write_text("Oggi studio Python\nDomani vado in vacanza", encoding="utf-8")
testo = percorso.read_text(encoding="utf-8")

print(f"Testo: {testo}")
print(f"Caratteri: {len(testo)}")
print(f"Parole: {len(testo.split())}")