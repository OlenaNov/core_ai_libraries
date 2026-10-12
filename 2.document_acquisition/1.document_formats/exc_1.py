
from pathlib import Path

folder = Path(__file__).parent
file_path = folder / "elenco.txt"
file_path.write_text("Mela\nPera\nBanana", encoding="utf-8")

try:
    content = file_path.read_text(encoding="utf=8")
    print(content)
    print(f"Rows: {len(content.split('\n'))}")

except Exception as e:
    print(f"Error: {e}")