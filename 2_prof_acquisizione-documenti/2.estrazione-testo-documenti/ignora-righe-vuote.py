#Traccia: crea un file con del testo e alcune righe vuote in mezzo. 
# Estrai solo le righe che contengono testo e stampa quante erano in totale e quante sono quelle utili.

from pathlib import Path

cartella = Path(__file__).parent
percorso = cartella / "con-vuote.txt"

percorso.write_text(
    "Titolo\n\nPrimo paragrafo\n\n\nSecondo paragrafo\n",
    encoding="utf-8"
)

testo = percorso.read_text(encoding="utf-8")
righe = testo.splitlines()

righe_utili = []
for riga in righe:
    if riga.strip() != "":
        righe_utili.append(riga)

print("Righe totali:", len(righe))
print("Righe con testo:", len(righe_utili))

for riga in righe_utili:
    print(riga)
