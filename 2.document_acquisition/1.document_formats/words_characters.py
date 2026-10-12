
from pathlib import Path

folder = Path(__file__).parent
path_file = folder / "write_file.txt"

content = path_file.read_text(encoding="utf-8")
print(content)
print(f"Characters: {len(content.split())}")
print(f"Words: {len(content.split())}")