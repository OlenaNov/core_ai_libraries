
#Traccia: estrai tutto il testo di esercizi.pdf,
# uniscilo in un'unica stringa e salvalo nel file esempio-estratto.txt.
# Stampa quanti caratteri hai salvato.

from pathlib import Path
from pypdf import PdfReader
from pypdf.errors import PdfReadError

def extract_and_save_pdf_text(pdf_path: Path, txt_path: Path) -> None:
    """Estrae tutto il testo da un file PDF, lo unisce in un'unica stringa
    e lo salva all'interno di un file di testo, stampando il totale dei caratteri.
    """
    try:
        if not pdf_path.exists():
            raise FileNotFoundError(f"Il file PDF'{pdf_path.name}' non è stato trovato.")

        reader = PdfReader(pdf_path)
        pages_text = []

        for idx, page in enumerate(reader.pages, start=1):
            text = page.extract_text()
            if text:
                pages_text.append(text)

        full_text = "\n".join(pages_text)

        txt_path.write_text(full_text, encoding="utf-8")

        print(f"Testo estratto con successo da '{pdf_path.name}'.")
        print(f"Caratteri totali salvati in '{txt_path.name}':  {len(full_text)}")
        
    except FileNotFoundError as e:
        print(f"Errore: {e}")
    except PdfReadError as e:
        print(f"Errore: Impossibile leggere il file PDF(potrebbe essere corrotto). Dettagli: {e}")
    except Exception as e:
        print(f"Errore imprevisto: {e}")


def main() -> None:
    folder = Path(__file__).parent
    pdf_file = folder / "example.pdf"
    txt_file = folder / "example_extracted.txt"

    extract_and_save_pdf_text(pdf_file, txt_file)

if __name__ == "__main__":
    main()

# folder = Path(__file__).parent
# pdf_reader = PdfReader(folder / "example.pdf")

# pages = []
# for page in pdf_reader.pages:
#     text = page.extract_text()
#     if text:
#         pages.append(text)

# print(pages)

# full_text = "\n".join(pages)

# (folder / "text_from_pdf.txt").write_text(full_text)