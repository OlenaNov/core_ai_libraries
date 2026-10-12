# TODO Switch!!!

# Traccia: scrivi la funzione leggi_documento(percorso) che legge un file 
# TXT, MD o DOCX in base all'estensione e restituisce il testo. 
# Per altre estensioni deve restituire Formato non supportato. 
# Provala con nota.txt, guida.md, primo.docx e report.pdf.

from pathlib import Path

def read_document(path):
    print(path)
    return path

try: 
    folder = Path(__file__).parent

except NameError:
    folder = Path.cwd()

file_name = input("File name: ").strip().lower()
try: 
    file_extension = Path(file_name).suffix
    path_file = folder / file_name
    content = read_document(path_file)
    print(f"Response: {content}")

except Exception as e:
    print("This file name isn't correct." 
          "{e}"
          )
    
