#Traccia: crea un listino.docx con una tabella di 2 righe e 2 colonne (nome e prezzo di due prodotti),
# poi estrai e stampa il testo di ogni cella.
from pathlib import Path
from docx import Document

cartella = Path(__file__).parent
percorso = cartella / "listino.docx"

documento = Document()

tabella = documento.add_table(rows=2, cols=2)
tabella.cell(0, 0).text = "Penna"
tabella.cell(0, 1).text = "1 euro"
tabella.cell(1, 0).text = "Quaderno"
tabella.cell(1, 1).text = "3 euro"

documento.save(percorso)

documento = Document(percorso)
for tabella in documento.tables:
    for riga in tabella.rows:
        celle = []
        for cella in riga.cells:
            celle.append(cella.text)
        print(" | ".join(celle))