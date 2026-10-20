#Traccia. Scrivi elenca_documenti(cartella) che restituisce, in ordine alfabetico, tutti i file con estensione .txt, .md, .html, .htm anche nelle sottocartelle, 
# ignorando maiuscole/minuscole nell'estensione e i file nascosti (nome che inizia con .).

from pathlib import Path

ESTENSIONI = {".txt", ".md", ".html", ".htm"}

def elenca_documenti(cartella):
    trovati = []
    for f in Path(cartella).rglob("*"):
        if (f.is_file()
                and f.suffix.lower() in ESTENSIONI
                and not f.name.startswith(".")):
            trovati.append(f)
    return sorted(trovati)

for f in elenca_documenti("documenti"):
    print(f)
