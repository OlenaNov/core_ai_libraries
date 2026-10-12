
from pathlib import Path
from typing import Optional
from pypdf import PdfReader
from pypdf.errors import PdfReadError

def extract_page_text(pdf_path: Path, target_page_num: int) -> Optional[str]:
    """Estrae il testo da una pagina specificata di un documento PDF in modo sicuro.

    Args:
        pdf_path (Path): Il percorso del file PDF.
        target_page_num (int): Il numero della pagina desiderata (partendo da 1).

    Returns:
        Optional[str]: Il testo della pagina se trovato, altrimenti None.
    """

    try:
        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)

        page_index = target_page_num - 1

        if 0 <= page_index < total_pages:
            page = reader.pages[page_index]
            return page.extract_text()
        else:
            print(f"Errore: La pagina {target_page_num} non esiste")
            return None

    except FileNotFoundError:
        print(f"Errore: Il file '{pdf_path}' non è stato trovato.")
        return None
    except PdfReadError as e:
        print(f"Errore: Impossibile leggere il file PDF (potrebbe essere corrotto o protetto). \nDettagli: {e}")
        return None
    except Exception as e:
        print(f"Errore imprevisto: {e}")
        return None

def main() -> None:
    folder = Path(__file__).parent
    pdf_file = folder / "example.pdf"

    target_page = 21

    print(f"Tentativo di estrazione della pagina {target_page} da '{pdf_file.name}'...")
    page_text = extract_page_text(pdf_file, target_page)

    if page_text:
        print(f"\n--- Contenuto Pagina {target_page} ---\n")
        print(page_text)

if __name__ == "__main__":
    main()