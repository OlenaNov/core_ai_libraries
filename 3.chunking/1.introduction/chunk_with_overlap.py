# TODO Rescrivere da run_tests e capire che fa
from typing import List

def chunk_characters(text: str, size:int, overlap: int = 0):
    """
    Splits text into chunks of 'size' characters, restarting each chunk 
    'overlap' characters before the end of the previous one.
    
    Logic explanation:
        - The step is 'size - overlap': without overlap it equals 'size', 
          with overlap it equals 'size - overlap' (e.g., 100 - 20 = 80).
        - range(0, len(text), step) generates the starting positions 'i'.
        - The slice 'text[i:i + size]' extracts the segment.
        - Note: the last chunk might be shorter because the text ends. 
          With large overlaps, a very short last chunk might be 
          entirely contained within the previous one (duplicated text).
    
    Args:
        text: The string to split.
        size: The fixed size of each chunk.
        overlap: The number of overlapping characters between adjacent chunks (default = 0).

    Returns:
        A list of strings containing the extracted chunks.

    Raises:
        TypeError: If text is not a string.
        ValueError: If size <= 0 or if overlap is invalid.
    """

    if not isinstance(text, str):
        raise TypeError("The 'text' parameter must be a string.")
    if size <= 0:
        raise ValueError("The chunk size must be greater than zero.")
    if not (0 <= overlap < size):
        raise ValueError("Overlap must be between 0 and size - 1.")

    step = size - overlap

    return [
        segment for i in range(0, len(text), step)
        if (segment := text[i:i + size]).strip()
    ]

def run_tests() -> None:
    """Executes the test suite with size=100 and overlaps of 0 and 20."""
    TEXT = "Python is a fantastic and flexible programming language. " * 10

    print("=== TEST WITH SIZE=100 AND OVERLAP 0 and 20 ===")
    for overlap_val in (0, 20):
        chunks = chunk_characters(TEXT, 100, overlap=overlap_val)
        print(f"Overlap: {overlap_val:2d} | N. Chunks: {len(chunks):2d} | Lengths: {[len(x) for x in chunks]}")

    print("\n=== OVERLAP VERIFICATION (OVERLAP = 20) ===")
    chunks = chunk_characters(TEXT, 100, overlap=20)
    
    if len(chunks) >= 2:
        last_20 = chunks[0][-20:]
        first_20 = chunks[1][:20]
        
        print(f"Last 20 characters of the first chunk: {repr(last_20)}")
        print(f"First 20 characters of the second chunk: {repr(first_20)}")
        print(f"Do the segments match perfectly? -> {last_20 == first_20}")
    else:
        print("The text is too short to perform multiple chunk tests.")


# Protected entry point: prevents automatic execution when imported as a module
if __name__ == "__main__":
    run_tests()