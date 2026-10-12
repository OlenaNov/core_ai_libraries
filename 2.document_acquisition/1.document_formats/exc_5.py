
from pathlib import Path

folder = Path(__file__).parent
path_file = folder / "guida_python.md"

try:
    content_list = path_file.read_text(encoding="utf-8").split("\n")
    for row in content_list:
        if row.startswith("#"):
            print(row)
    
except Exception as e:
    print(e)