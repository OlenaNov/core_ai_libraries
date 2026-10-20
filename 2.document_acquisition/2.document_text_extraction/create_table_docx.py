
from pathlib import Path
from typing import Dict, List, Any
from docx import Document


def create_report_table(file_path: Path, data: List[Dict[str, Any]]) -> None:
    """Crea un documento Word, genera una tabella basata sui dati forniti
    e la salva nel percorso specificato.

    Args:
        file_path (Path): Il percorso completo in cui salvare il file Word.
        data (List[Dict[str, Any]]): Lista di dizionari contenuti le righe del report.

    Raises:
        ValueError: Se la lista dei dati è vuota.
        OSError: Se si verificano problemi durante il salvataggio del file.
    """
    if not data:
        raise ValueError("Impossibile generare la tabella: la lista dei dati è vuota.")
    
    doc = Document()

    keys = list(data[0].keys())
    
    table = doc.add_table(rows=len(data) + 1, cols=len(keys))

    header_cells = table.rows[0].cells
    for col_idx, key in enumerate(keys):
        header_cells[col_idx].text = str(key)


    for row_idx, item in enumerate(data, start=1):
        row_cells = table.rows[row_idx].cells
        for col_idx, key in enumerate(keys):

            row_cells[col_idx].text = str(item.get(key, ""))

    try:
        doc.save(file_path)
        print(f"Report salvato con successo in {file_path.resolve()}")
    except OSError as e:
        print(f"Errore critico durante il salvataggio del file: {e}")
        raise

def main() -> None:
    
    folder = Path(__file__).parent
    file_path = folder / 'report_table.docx'

    report_data = [
    {"Item": "Monitor", "Price_€": 139, "Quantity": 13},
    {"Item": "Keyboard", "Price_€": 45, "Quantity": 25},
    {"Item": "Mouse", "Price_€": 25, "Quantity": 40},
    {"Item": "Laptop", "Price_€": 850, "Quantity": 8},
    {"Item": "Headset", "Price_€": 60, "Quantity": 15},
    {"Item": "Webcam", "Price_€": 75, "Quantity": 12},
    {"Item": "Printer", "Price_€": 120, "Quantity": 5},
    {"Item": "Desk Chair", "Price_€": 199, "Quantity": 7},
    {"Item": "USB-C Hub", "Price_€": 35, "Quantity": 30},
    {"Item": "External SSD", "Price_€": 110, "Quantity": 20},
]

    try:
        create_report_table(file_path, report_data)
    except Exception as e:
        print(f"Processo interrotto a causa di un errore: {e}")


if __name__ == "__main__":
    main()