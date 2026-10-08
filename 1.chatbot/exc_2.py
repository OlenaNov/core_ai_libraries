
# Traccia: crea l'assistente virtuale di una libreria con un'istruzione che ne definisce lo scopo e il tono. 
# Inviagli 6 messaggi, di cui 2 fuori tema, e osserva come reagisce.

from chatbot_def import generate_ai_response

print(f"Buongiorno, sono il tuo assistente virtale")
query = input("Che informazione vuoi trovare oggi?").split()
print("""Che tipo di risposta vuoi ottenere? 
    1 - Rispondi sempre in modo chiaro, cortese e conciso.
    2 - Se non sai una risposta, ammettilo senza inventare.
    3 - Usa elenchi puntati e grassetti per facilitare la lettura.
    4 - Concludi con una breve domanda utile per proseguire.
    5 - Comunica esclusivamente in italiano.
    6 - Non chiedere né memorizzare dati personali sensibili.
    """
)
idx_instructions = int(input("Premi il numero del tono: ").strip())

instructions = [
    "Rispondi sempre in modo chiaro, cortese e conciso.",
    "Se non sai una risposta, ammettilo senza inventare.",
    "Usa elenchi puntati e grassetti per facilitare la lettura.",
    "Concludi con una breve domanda utile per proseguire.",
    "Comunica esclusivamente in italiano.",
    "Non chiedere né memorizzare dati personali sensibili."
]

response = generate_ai_response(query, instructions[idx_instructions])

print(f"\33[1;92m{response}")
