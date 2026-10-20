from pathlib import Path

cartella = Path(__file__).parent

# Creazione dei file di prova
(cartella/ "nota.txt").write_text(
    "Oggi studio Python e documenti.",
    encoding="utf-8"
)
(cartella / "guida.md").write_text(
    "# Guida\nPython è **facile**.",
    encoding="utf-8"
)


def leggi_file(nome_file):
    percorso = cartella / nome_file
    return percorso.read_text(encoding="utf-8")


file_da_leggere = ["nota.txt", "guida.md"]

for nome in file_da_leggere:
    testo = leggi_file(nome)
    parole = testo.split()

    print("File:", nome)
    print("Testo:", testo)
    print("Numero di parole:", len(parole))
    print("-" * 30)