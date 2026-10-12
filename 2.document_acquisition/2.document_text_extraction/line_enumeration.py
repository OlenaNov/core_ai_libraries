
import sys
from pathlib import Path
from typing import Optional


sys.path.append(str(Path(__file__).resolve().parents[2] / "1.chatbot"))

try: 
    from chatbot_def import generate_ai_response
except ImportError as e:
    print(f"Errore critico: Impossibile importare 'chatbot_def'.\nDettagli: {e}")
    sys.exit(1)

def fetch_and_save_poem(file_path: Path) -> Optional[str]:
    """Richiede una poesia tramite IA e la memorizza su file di testo.

    Args:
        file_path(Path): Il percorso del file in cui salvare la poesia.

    Returns: 
        Optional[str]: Il contenuto delaa poesia se generato con successo, altrimenti None.
    """
    prompt = "Inviami una famosa poesia italiana, al massimo di 120 righe"
    instruction = "La risposta deve contenere solo la poesia, con il titolo e alla fine l'autore, niente più"

    try:
        print("Generazione della poesia tramite IA in corso...")
        content = generate_ai_response(prompt, instruction)

        file_path.write_text(content, encoding="utf-8")
        return content

    except Exception as e:
        print(f"Errore durante la generazione o la scrittura del file: {e}")
        return None


def print_numbered_poem(poem_text: str) -> None:
    """"Stampa a scermo la poesia gestendo le righe vuote e numerando quelle valide"""
    line_number = 1
    for row in poem_text.splitlines():
        if not row.strip():
            print()
        else: 
            print(f"{line_number} {row}")
            line_number += 1


def calculate_poem_length_statistics(poem_text: str) -> None:
    """Calcola le statistiche di una poesia, estraendo titolo (prima righa),
    autore (ultima riga) e contando le righe di testo e quelle vuote.
    """
    lines = poem_text.splitlines()
    if not lines:
        print("Il testo della poesia è vuoto.")
        return
    
    title_string = lines[0].strip()
    author_string = lines[-1].strip()

    empty_string_count = 0
    poem_length = 0

    for idx, line in enumerate(lines):
        if idx == 0 or idx == len(lines) - 1:
            continue

        if not line.strip():
            empty_string_count += 1
        else:
            poem_length += 1

    print(f"Totale righe nel file: {len(lines)}")
    print(f" La poesia '{title_string}' di {author_string} contiene {poem_length} righe di testo")
    print(f"Le righe vuote sono {empty_string_count}")


def main() -> None:
    folder = Path(__file__).parent
    file_path = folder / "numbered_lines.txt"

    poem_content = fetch_and_save_poem(file_path)
    if not poem_content:
        return

    print("\n --- Risultato formato ---\n")
    print_numbered_poem(poem_content)
    calculate_poem_length_statistics(poem_content)


if __name__ == "__main__":
    main()





