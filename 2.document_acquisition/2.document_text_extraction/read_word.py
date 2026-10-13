#Traccia: apri primo.docx creato in precedenza e stampa il testo di ogni paragrafo.

from pathlib import Path
from typing import Optional
from docx import Document
from docx.opc.exceptions import PackageNotFoundError


def print_docx_paragraphs(file_path: Path) -> None:
    """Legge un file Word (.docx) e stampa a schermo il testo di ogni paragrafo.
    
    Args:
        file_path (Path): Il percorso completo del file Word da leggere.
    """

    try:
        if not file_path.exists():
            raise FileNotFoundError(f"Il file '{file_path_name}'  non è stato trovato nella cartella.")

        doc = Document(file_path)

        print(f"\n === Contenuto del documento: {file_path.name} ===")
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                print(paragraph.text)

    except FileNotFoundError as e:
        print(f"Errore: {e}")
    except PackageNotFoundError:
        print(f"Errore: Il file '{file_path.name}' non è documento Word valido o risulta corrotto.")
    except Exception as e:
        print(f"Errore imprevisto durante la lettura del file {e}")


def main() -> None:
    folder = Path(__file__).parent
    file_path = folder / "confirmation_letter.docx"

    print_docx_paragraphs(file_path)

if __name__ == "__main__":
    main()