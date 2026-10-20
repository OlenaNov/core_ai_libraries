#Traccia: hai la lista ["nota.txt", "guida.md", "report.pdf", "contratto.docx"]. 
# Per ogni nome stampa il nome e la sua estensione.

from pathlib import Path

nomi_file = ["nota.txt", "guida.md", "report.pdf", "contratto.docx"]

for nome in nomi_file:
    estensione = Path(nome).suffix
    print(nome, "->", estensione)
