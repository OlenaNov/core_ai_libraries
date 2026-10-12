import sys
from pathlib import Path

# Usa parents[2] per raggiungere 'core_ai_libraries' e puntare a '1.chatbot'
sys.path.append(str(Path(__file__).resolve().parents[2] / "1.chatbot"))

from chatbot_def import generate_ai_response

folder = Path(__file__).parent
file_path = folder / "pandas_introdaction.md"

content = generate_ai_response("Che cos'è Pandas", "Rispondi in formato md")

file_path.write_text(content, encoding="utf-8")

text = file_path.read_text(encoding="utf-8")
paragraphs_list = []

for row in text.splitlines():
    if row.startswith("#"):
        continue
    if row.strip() == "":
        continue
    paragraphs_list.append(row)

for paragraph in paragraphs_list:
    print(paragraph)