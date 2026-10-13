
from pathlib import Path
from docx import Document

report_dict = [
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


def create_table(file_path: Path) -> None:

    doc = Document()
    keys = ["Item", "Price_€", "Quantity"]
    
    table = doc.add_table(rows=len(report_dict) + 1, cols=len(keys))

    header_cells = table.rows[0].cells
    for i, key in enumerate(keys):
        header_cells[i].text = str(key)


    for idx, item in enumerate(report_dict, start=1):
        row_cells = table.rows[idx].cells

        for k, key in enumerate(keys):
            row_cells[k].text = str(item[key])
            print(f"Riga {idx}, Colonna {k}: {item[key]}")
    doc.save(file_path)


def main() -> None:
    folder = Path(__file__).parent
    docx_path = folder / 'report_table.docx'

    create_table(docx_path)


if __name__ == "__main__":
    main()