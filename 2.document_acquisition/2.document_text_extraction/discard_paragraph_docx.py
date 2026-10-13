
from pathlib import Path
from docx import Document


def create_docx(docx_path: Path) -> None:
    """Crea un nuovo documento Word da zero e inserisce una lista di paesi."""

    countries_list = ["Italia", "Grecia", "Spagna", "Ucraina", "Germania"]
    
    doc = Document()

    for country in countries_list:
        doc.add_paragraph(f"{country}")
        doc.add_paragraph("")
        doc.add_paragraph("")

    doc.save(docx_path)

def print_docx_and_statistics(docx_path: Path) -> None:
    """Legge il documento Word, stampa il testo e calcola le statistiche dei paragrafi."""
    try:
        doc = Document(docx_path)
        total_paragraphs = len(doc.paragraphs)
        empty_paragraphs = 0

        print(f"\n--- Contenuto del documento: {docx_path.name} ---")

        for paragraph in doc.paragraphs:
            text = paragraph.text
            print(text)

            if not text.strip():
                empty_paragraphs += 1
                
        print("\n--- Statistiche ---")
        print(f"Paragrafi vuoti: {empty_paragraphs}")
        print(f"Paragrafi totali: {total_paragraphs}")

    except Exception as e:
        print(f"Errore durante la lettura del file: {e}")



def main() -> None:
    folder = Path(__file__).parent
    docx_path = folder / 'discard_example.docx'

    create_docx(docx_path)
    print(f"Il file è stato creato con successo.")

    print_docx_and_statistics(docx_path)

    
if __name__ == "__main__":
    main()