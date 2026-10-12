
from pathlib import Path

folder = Path(__file__).parent
path_file = folder / "diario.txt"

path_file.write_text("Prima riga", encoding="utf-8")

try:
    content = path_file.read_text(encoding="utf-8")
    new_row = "\nSeconda riga"
    content += new_row
    path_file.write_text(content, encoding="utf-8")
    
except Exception as e:
    print(e)