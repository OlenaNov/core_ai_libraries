
from pathlib import Path

folder = Path(__file__).parent
path_file = folder / "guida_python.md"

path_file.write_text("# Guida rapida a Python\n\nPython è un linguaggio di programmazione **versatile e potente**, molto apprezzato sia nello sviluppo web che nell'ambito dell'intelligenza artificiale. Grazie alla sua sintassi pulita, permette di **scrivere codice leggibile** e di prototipare applicazioni in tempi rapidi.", encoding="utf-8")

try: 
    content = path_file.read_text(encoding="utf-8")
    print(content)
except Exception as e:
    print(e)