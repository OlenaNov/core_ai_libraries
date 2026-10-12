from pathlib import Path
from docx import Document

cartella = Path(__file__).parent


def leggi_documento(percorso):
    estensione = percorso.suffix.lower()

    if estensione == ".txt" or estensione == ".md":
        return percorso.read_text(encoding="utf-8")
    elif estensione == ".docx":
        documento = Document(percorso)
        paragrafi = []
        for paragrafo in documento.paragraphs:
            paragrafi.append(paragrafo.text)
        return "\n".join(paragrafi)
    else:
        return "Formato non supportato"


nomi_file = ["nota.txt", "guida.md", "primo.docx", "report.pdf"]

for nome in nomi_file:
    percorso = cartella / nome
    print("File:", nome)
    if percorso.exists():
        print(leggi_documento(percorso))
    else:
        print("File non trovato")
    print("-" * 30)

