"""Grounded answer composition from retrieved evidence."""

from rag_app.models import SearchResult


def generate_answer(
        question: str,
        results: list[SearchResult],
        minimum_score: float = 0.05,
) -> str:
    """Compose an extractive answer and cite the retrieved source chunks.
    
    The function deliberately does not claim to be LLM. It returns evidence
    snippets so the prototype remains transparent and fully offline.
    """
    if not question or not question.strip():
        raise ValueError("question cannot be empty")
    if not 0 <= minimum_score <= 1:
        raise ValueError("minimum score must be between zero and one")
    if not results:
        return "Non ho trovato informazioni pertinenti nei documenti indicizzati."

    relevant_results = [
        result for result in results
        if result.score >= minimum_score
    ]
    if not relevant_results:
        return (
            "Non ho trovato evidenze sufficientamente pertinenti per rispondere."
            "Prova a riformulare la domanda."
        )

    answer_lines = [
        "Ho trovato queste informazioni nei documenti disponibili:"
    ]
    for result in relevant_results:
        chunk = result.chunk
        answer_lines.append(
            f"- {chunk.text} [Fonte: {chunk.source}, "
            f"chunk: {chunk.chunk_id}, similatità: {result.score:.3f}]"
        )
        answer_lines.append(
            "Nota: questa versione restituisce estratti recuperati;"
            "non usa ancora un modello linguistico per sintetizzare una risposta."
        )
        return "\n".join(answer_lines)
    