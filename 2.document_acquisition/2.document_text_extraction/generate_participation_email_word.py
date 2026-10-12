
import sys
from pathlib import Path
from typing import Optional
from docx import Document

sys.path.append(str(Path(__file__).resolve().parents[2] / "1.chatbot"))

try:
    from chatbot_def import generate_ai_response
except ImportError as e:
    print(f"Errore: Impossibile importare 'chatbot_def'.\nDettagli: {e}")
    sys.exit(1)


def generate_and_save_email(file_path: Path) -> Optional[str]:
    """"Genera una mail di conferma tramite IA, formatta la prima riga come Heading 2
    con una sezione, salva il documento in Word (.docx) e restituisce il testo.
    """

    prompt = (
        "Genera una mail di conferma della partecipazione del corso di Intelligenza Artificiale, "
        "indicando che il calendario ed il programma didattico sono in allegato con la lunghezza massima di 300 caratteri."
    )    
    instruction = "Usa il tono cordiale e gentile"

    try:  
        print("Generazione dell'email in corso...")
        content = generate_ai_response(prompt, instruction)

        lines = content.strip().splitlines()

        if not lines:
            print("Errore: Il testo generato è vuoto.")
            return None

        heading_text = lines[0]
        body_paragraphs = lines[1:] if len(lines) > 1 else ["Contenuto di conferma corso."]

        doc = Document()

        doc.add_heading(f"Sezione: {heading_text}", level=2)

        for paragraph_text in body_paragraphs:
            if paragraph_text.strip():
                doc.add_paragraph(paragraph_text)

        doc.save(file_path)
        print(f"Documento salvato con successo in: {file_path.name}")
        
        return content

    except Exception as e:
        print(f"Errore durante la generazione o il salvataggio: {e}")
        return None


def print_email_confirm(content: str) ->None:
    """Stampa a schermo il contenuto dell'email formattato."""
    if content:
        print(content)


def main() -> None:
    folder = Path(__file__).parent
    file_path = folder / "confirmation_letter.docx"

    letter_content = generate_and_save_email(file_path)
    
    if not letter_content:
        return

    print("\n--- Lettera di conferma ---\n")
    print_email_confirm(letter_content)

if __name__ == "__main__":
    main()