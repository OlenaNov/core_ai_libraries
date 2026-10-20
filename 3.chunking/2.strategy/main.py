
# Importazione pulita dei moduli dalla cartella strategy
from tokenizers import split_sentences, tokenize_words, tokenize_subwords
from chunking import chunk_hybrid, chunk_by_words

DOC = """# Guida ai resi
## Come richiedere il reso
Il cliente può restituire il prodotto entro quattordici giorni dalla consegna. La richiesta si invia dall'area personale.
## Rimborso
Il rimborso avviene entro sette giorni dal ricevimento del reso. Le spese di spedizione restano a carico del cliente."""


if __name__ == "__main__":
    print("=== TEST TOKENIZZAZIONE ===")
    sample_text = "La PEC ha valore legale."
    print(f"Frasi: {split_sentences(sample_text)}")
    print(f"Parole: {tokenize_words(sample_text)}")


    print("\n=== TEST CHUNKING IBRIDO ===")
    chunks = chunk_hybrid(DOC, max_chars=100)
    for i, c in enumerate(chunks, 1):
        print(f"Chunk {i} [{c['title']}]: {c['text']} (len: {len(c['text'])})")


    print("\n=== TEST CHUNKING SUL CONFINE DI PAROLA (chunk_by_words) ===")
    test_text = (
        "Il cliente può restituire il prodotto entro quattordici giorni dalla consegna. "
        "La richiesta si invia dall'area personale."
    )
    word_chunks = chunk_by_words(test_text, size=30)
    for i, chunk in enumerate(word_chunks, 1):
        print(f"Chunk {i:2d} (len: {len(chunk):2d}): {repr(chunk)}")