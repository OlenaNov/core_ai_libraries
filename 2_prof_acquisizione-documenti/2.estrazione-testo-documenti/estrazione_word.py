#Traccia: crea un file lettera.docx con tre paragrafi,
# poi aprilo e stampa il testo di ogni paragrafo con il suo numero.
from pathlib import Path
from docx import Document

cartella = Path(__file__).parent
percorso = cartella / "lettera.docx"

documento = Document()
documento.add_paragraph("Gentile cliente,")
documento.add_paragraph("la ringraziamo per la richiesta.")
documento.add_paragraph("Cordiali saluti.")

documento.save(percorso)

documento = Document(percorso)
numero = 1

for paragrafo in documento.paragraphs:
    print(numero, ":", paragrafo.text)
    numero = numero + 1