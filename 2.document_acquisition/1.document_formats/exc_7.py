
from pathlib import Path
from pypdf import PdfReader

folder = Path(__file__).parent
path_file = folder / "example.pdf"

try:
    reader_pages = PdfReader(path_file).pages
    content = ""
    for page in reader_pages:
        page_content = page.extract_text()
        content += page_content

    print(f"Total words: {len(content.split())}")
    

except Exception as e:
    print(e)