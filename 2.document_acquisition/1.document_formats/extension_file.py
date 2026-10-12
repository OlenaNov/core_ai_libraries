
from pathlib import Path

nomi_file = ["nota.txt", "guida.md", "report.pdf", "contratto.docx"]

for nome in nomi_file:
    estensione = Path(nome).suffix
    print(f"{nome} -> {estensione}")