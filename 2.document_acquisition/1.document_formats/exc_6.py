
from pathlib import Path
from pypdf import PdfReader

folder = Path(__file__).parent
path_file = folder /"example.pdf"

try:
    reader = PdfReader(path_file)
    print(f"Total pages: {len(reader.pages)}")
    print(f"The first page: {reader.pages[0].extract_text()}")

except Exception as e:
    print(e)