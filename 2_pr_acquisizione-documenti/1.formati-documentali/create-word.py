from pathlib import Path
from docx import Document

cartella = Path(__file__).parent

documento = Document()
documento.add_heading("Il mio primo documento", level=1)
documento.add_paragraph("Questo file Word è stato creato con Python.")
documento.save(cartella / "primo.docx")

print("File creato")


