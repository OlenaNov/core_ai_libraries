#Traccia: crea un file con del testo e alcune righe vuote in mezzo. 
# Estrai solo le righe che contengono testo e stampa quante erano in totale e quante sono quelle utili.

from pathlib import Path

folder = Path(__file__).parent
file_path = folder / "con-vuote.txt"

try: 
    file_path.write_text(
        "Titolo\n\nPrimo paragrafo\n\n\nSecondo paragrafo\n",
        encoding="utf-8"
    )

    text = file_path.read_text(encoding="utf-8")
    rows = text.splitlines()

    rows_utils = []
    for row in rows:
        if row.strip() != "":
            rows_utils.append(row)

    print(f"Righe totali: {len(rows)}")
    print(f"Righe con testo: {len(rows_utils)}")

except Exception as e:
    print(e)