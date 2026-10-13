#Traccia: crea un appunti.docx con tre paragrafi di testo e due paragrafi vuoti in mezzo.
# Estrai solo i paragrafi con testo e stampa quanti sono sui totali.
from pathlib import Path
from docx import Document

cartella = Path(__file__).parent
percorso = cartella / "nazioni.docx"

documento = Document()

documento.add_paragraph("ITALIA")
documento.add_paragraph("")
documento.add_paragraph("SPAGNA")
documento.add_paragraph("")
documento.add_paragraph("GERMANIA")

documento.save(percorso)

documento = Document(percorso)
paragrafi_utili = []

for paragrafo in documento.paragraphs:
    if paragrafo.text.strip() != "":
        paragrafi_utili.append(paragrafo.text)
        
print("Paragrafi totali:", len(documento.paragraphs))
print("Paragrafi con testo:", len(paragrafi_utili))