
from pathlib import Path
from docx import Document

folder = Path(__file__).parent
file_path = folder / "example.docx"

document = Document()
document.add_paragraph("Gentile cliente,")
document.add_paragraph("la ringraziamo per la richiesta.")
document.add_paragraph("Cordiali saluti.")

document.save(file_path)

document = Document(file_path)
number = 1

for paragraph in document.paragraphs:
    print(f"Paragrafo numero {number}: \n{paragraph.text}\n")
    number += 1