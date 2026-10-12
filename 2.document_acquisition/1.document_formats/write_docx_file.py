
from pathlib import Path

folder = Path(__file__).parent
file_path = folder / "write.docx"
file_path.write_text("Domani studio Python", encoding="utf-8")

content_file = file_path.read_text(encoding="utf-8")

print(content_file)