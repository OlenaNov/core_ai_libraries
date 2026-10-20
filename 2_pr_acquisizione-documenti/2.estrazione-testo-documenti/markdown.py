#Traccia: crea un file Markdown con titoli (righe che iniziano con #) e paragrafi. 
# Estrai solo i paragrafi e stampali, escludendo titoli e righe vuote.

from pathlib import Path

cartella = Path(__file__).parent
percorso = cartella / "manuale.md"

contenuto = "# Manuale\nBenvenuto nel manuale.\n## Uso\nPremi il pulsante.\n### Argomento del giorno\nEstrazione del testo"
percorso.write_text(contenuto, encoding="utf-8")

testo = percorso.read_text(encoding="utf-8")

paragrafi = []
for riga in testo.splitlines():
    if riga.startswith("#"):
        continue
    if riga.strip() == "":
        continue
    paragrafi.append(riga)

for paragrafo in paragrafi:
    print(paragrafo)
