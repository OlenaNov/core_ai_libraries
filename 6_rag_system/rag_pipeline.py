
"""
Advanced Production-Grade RAG Data Engineering Pipeline.
"""

import hashlib
import logging
import math
import re
import tempfile
import unicodedata
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ServerError


# Configure structured logging 
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logger = logging.getLogger("AdvancedRAGPipeline")

# Load environment variables
load_dotenv()

# Initialize Gemini Client
client = genai.Client()

# Configuration Constants
MODEL_TEXT = "gemini-3.5-flash"
MODEL_EMBEDDING = "gemini-embedding-2"
DIMENSION = 768
NAMESPACE_DOCUMENT = uuid.UUID("6f1d2c9e-8b34-4a57-9c0e-2d7a41b5e6f3")
MANDATORY_METADATA = ("title", "date")


# ==========================================
# 1. TEXT UTILITIES & EMBEDDINGS ENGINE
# ==========================================

def compute_text_embedding(text: str, dim: int = DIMENSION) -> List[float]:
    """
    Compute a numerical embedding vector for a given text using Gemini API.
    """
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Input text must be a non-empty string.")

    try:
        response = client.models.embed_content(
            model=MODEL_EMBEDDING,
            contents=text,
            config=types.EmbedContentConfig(output_dimensionality=dim),
        )
        return response.embeddings[0].values

    except Exception as e:
        logger.error(f"Failed to generate embedding: {e}")
        raise


def compute_document_embedding(title: str, text: str, dim: int = DIMENSION) -> List[float]:
    """Compute embedding for document chunks using title-text semantic formatting."""
    formatted_content = f"title: {title} | text: {text}"
    return compute_text_embedding(formatted_content, dim=dim)


def compute_query_embedding(query: str, dim: int = DIMENSION) -> List[float]:
    """Compute embedding for user queries optimized for retrieval."""
    cleaned_query = " ".join(query.split())
    if not cleaned_query:
        raise ValueError("Query cannot be empty or contain only whitespace.")

    formatted_query = f"task: question-answering | query: {cleaned_query}"
    return compute_text_embedding(formatted_query, dim=dim)


def normalize_text(text: str) -> str:
    """Normalize text using NFC unicode normalization and collapse extra whitespace."""
    if not isinstance(text, str):
        raise TypeError("Input must be a string.")

    normalized_text = unicodedata.normalize("NFC", text)
    return " ".join(normalize_text.split())


def text_fingerprint(text: str) -> str:
    """Compute a SHA-256 cryptographic fingerprint for content verification."""
    return hashlib.sha256(text.encode("UTF-8")).hexdigest()


def generate_document_id(relative_path: str) -> str:
    """Generate a deterministic UUIDv5 based on normalized relative path."""
    canonical_path = relative_path.strip().lower()
    return str(uuid.uuid5(NAMESPACE_DOCUMENT, canonical_path))


# ==========================================
# 2. FILE INGESTION & PARSING PIPELINE
# ==========================================

def list_files(directory: Path, extensions: Tuple[str,  ...] = (".txt", ".md")) -> List[Path]:
    """Recursively search for files matching allowed extensions in a directory."""
    found_files = []
    for path in directory.rglob("*"):
        if path.is_file() and path.suffix.lower() in extensions:
            found_files.append(path)
    return sorted(found_files)


def read_text_file(path: Path) -> str:
    """Read a test file ensuring UTF-8 encoding with explicit error handling."""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        logger.error(f"Failed to decode file {path.name} with UTF-8 encoding.")
        raise ValueError("Invalid file encoding (UTF-8 expected).")


def split_header(content: str) -> Tuple[str, str, str]:
    """
    Split document into title, version/date row, and body content.
    Expects at least 3 lines.
    """
    lines = content.splitlines()
    if len(lines) < 3:
        raise ValueError("Missing structured header (min 3 lines required).")

    title = lines[0].lstrip("# ").strip()
    version_row = lines[1].strip()
    body = " ".join(lines[2:])
    return title, version_row, body


def extract_metadata(title: str, version_row: str) -> Dict[str, Optional[str]]:
    """Extract date and version number using regular expressions."""
    date_match = re.search(r"(\d{2})/(\d{2})/(\d{4})", version_row)
    version_match = re.search(r"[Vv]ersione\s+(\d+(?:\.\d+)*)", version_row)

    formatted_date = None
    if date_match:
        day, month, year = date_match.groups()
        formatted_date = f"{year}-{month}-{day}"

    return {
        "title": title,
        "version": version_match.group(1) if version_match else None,
        "date": formatted_date
    }


def validate_mandatory_metadata(metadata: Dict[str, Optional[str]]) -> List[str]:
    """Return a list of missing mandatory metadata fields."""
    return [field for field in MANDATORY_METADATA if not metadata.get(field)]


# ==========================================
# 3. CHUNKING & INDEXING PIPELINE
# ==========================================

def create_chunks(doc_id: str, body: str, metadata: Dict[str, Any], max_chars: int = 80) -> List[Dict[str, Any]]:
    """Split document body into sentence-level chunks respecting maximum character limits."""
    sentences =[f.strip() + "." for f in body.split(".") if f.strip()]
    groups, current_chunk = [], ""

    for sentence in sentences:
        if current_chunk and len(current_chunk) + 1 + len(sentence) > max_chars:
            groups.append(current_chunk)
            current_chunk = sentence
        else:
            current_chunk = (current_chunk + " " + sentence).strip()

    if current_chunk:
        groups.append(current_chunk)

    return [
        {
            **metadata,
            "id": f"{doc_id}_{i:03d}",
            "doc_id": doc_id,
            "text": text
         }
         for i, text in enumerate(groups)
    ]


def build_vector_index(chunks: List[Dict[str, Any]], dim: int = DIMENSION) -> List[Dict[str, Any]]:
    """Build the complete vector index computing embeddings for all chunks."""
    index = []
    for chunk in chunks:
        vector = compute_document_embedding(chunk["title"], chunk["text"], dim=dim)
        index.append({**chunk, "vector": vector})

    logger.info(f"Vector index successfully built with {len(index)} items.")
    return index


# ==========================================
# 4. ORCHESTRATION & DEMO EXECUTION
# ==========================================

def main() -> None:
    """Main execution entry point demonstrating the advanced data engineering pipeline."""

    # Setup temporary directory with structured documents
    base_dir = Path(tempfile.mkdtemp()) 
    (base_dir / "faq").mkdir()

    (base_dir / "resi.txt").write_text(
        "Politica dei resi\nVersione 2.1 - 03/10/2026\nIl reso è gratuito entro quattordici giorni dalla consegna. Il prodotto deve essere integro.",
        encoding="utf-8"
    )

    (base_dir / "rimborsi.txt").write_text(
        "Rimborsi\nVersione 1.0 - 15/09/2026\nIl rimborso arriva entro sette giorni dal ricevimento del reso. Il rimborso usa lo stesso metodo di pagamento.",
        encoding="utf-8"
    )

    (base_dir / "faq" / "pagamenti.txt").write_text(
        "Pagamenti\nVersione 1.1 - 20/09/2026\nSi accettano carta di credito e bonifico bancario.",
        encoding="utf-8"
    )

    # Pipeline execution flow
    files = list_files(base_dir)
    logger.info(f"Discovered {len(files)} valid documents.")

    all_chunks = []
    for file_path in files:
        rel_path = file_path.relative_to(base_dir).as_posix()
        doc_id = generate_document_id(rel_path)

        raw_content = read_text_file(file_path)
        title, version_row, body = split_header(raw_content)
        metadata = extract_metadata(title, version_row)

        missing = validate_mandatory_metadata(metadata)
        if missing:
            logger.warning(f"Skipping {rel_path}: missing mandatory metadata fields {missing}")
            continue

        metadata["source"] = rel_path
        metadata["fingerprint"] = text_fingerprint(body)

        chunks = create_chunks(doc_id, body, metadata, max_chars=120)
        all_chunks.extend(chunks)

    # Build vector index
    vector_index = build_vector_index(all_chunks)
    logger.info(f"Indexing complete. Total indexed chunks ready for retrieval: {len(vector_index)}")

if __name__ == "__main__":
    main()






