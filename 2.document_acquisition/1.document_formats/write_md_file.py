
from pathlib import Path

folder = Path(__file__).parent
file_path = folder / "write_file.md"
file_path.write_text("#Oggi studio Python, magari", encoding="utf=8")

content_file = file_path.read_text(encoding="utf-8")

print(f"Content {content_file}")