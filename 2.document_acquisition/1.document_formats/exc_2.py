
from pathlib import Path

folder = Path(__file__).parent
path_file = folder / "write_file.txt"

context = path_file.read_text(encoding="utf-8")
print(context)

if "Python" in context:
    print("Trovata")
else:
    print("Non trovata")