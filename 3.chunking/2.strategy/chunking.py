
from typing import List, Dict
from tokenizers import split_sentences

def chunk_by_titles(doc: str) -> List[Dict[str, str]]:
    """Divide un documento in sezioni basandosi sui titoli (righe che iniziano con #)."""
    if not isinstance(doc, str):
        raise TypeError("The 'doc' parameter must be a string")

    sections = []
    title = None
    lines = []

    for line in doc.splitlines():
        if line.startswith("#"):
            if "".join(lines).strip():
                sections.append({
                    "title": title,
                    "text": "\n".join(lines).strip()
                })
            title = line.lstrip("#").strip()
            lines = []
        else:
            lines.append(line)

    if "".join(lines).strip():
        sections.append({
            "title": title,
            "text": "\n".join(lines).strip()
        })
    return sections


def chunk_hybrid(doc: str, max_chars: int) -> List[Dict[str, str]]:
    """Divide per titoli e poi suddivide per frasi solo le sezioni più lunghe di max_chars."""
    result = []

    for section in chunk_by_titles(doc):
        if len(section["text"]) <= max_chars:
            parts = [section["text"]]
        else:
            parts = split_sentences(section["text"])

        for part in parts:
            result.append({
                "title": section["title"],
                "text": part
            })

    return result


def chunk_by_words(text: str, size: int) -> List[str]:
    """Divide il testo a ogni spazio e restituisce le parole"""
    if not isinstance(text, str):
        raise TypeError("The 'text' parameter must be a string.")
    if size <= 0:
        raise ValueError("The 'size' parameter must be greater than zero.")

    chunks = []
    start = 0
    text_len = len(text)

    while start < text_len:
        end = min(start + size, text_len)

        if end < text_len:
            cut = text.rfind(" ", start, end)
            if cut > start:
                end = cut

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        start = end

    return chunks

def chunk_fixed(text: str, size: int, overlap: int = 0) -> List[str]:
    """
    Taglia il testo a intervalli regolari in chunk di dimensione fissa 'dim',
    gestendo un eventuale 'overlap' tra i blocchi ed evitando chunk vuoti.
    """
    if not isinstance(text, str):
        raise TypeError("The 'text' parameter must be a string.")
    if size <= 0:
        raise ValueError("The 'size' parameter must be greater than zero")
    if not (0 <= overlap < size):
        raise ValueError("Overlap must be between 0 and size - 1.")

    step = size - overlap
    
    return [
        segment for i in range(0, len(text), step)
        if (segment := text[i:i + size]).strip()
    ]

# # todo if __name__ == "__main__":
#     alphabet = "abcdefghijklmnopqrstuvwxyz"
#     print(chunk_fixed(alphabet, 10))