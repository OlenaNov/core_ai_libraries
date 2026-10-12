
from pathlib import Path
from docx import Document

try:
    folder = Path(__file__).parent
except NameError:
    folder = Path.cwd()


path_file = folder /"primo.docx"

doc = Document()

doc.add_heading("Guida Rapida a Python")
doc.add_paragraph("Python è un linguaggio di programmazione versatile e potente, molto apprezzato sia nello sviluppo web che nell'ambito dell'intelligenza artificiale.")

doc.save(path_file)
print(f"The file was created: {path_file}")