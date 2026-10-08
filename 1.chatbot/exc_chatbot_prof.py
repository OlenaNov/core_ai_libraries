from gemini_utils import chiedi

istruzione = "Rispondi sempre in italiano, in una sola frase, come se parlassi a un bambino."

domande = [
    "Che cos'è un algoritmo?",
    "Che cos'è internet?",
    "Che cos'è una password?",
    "Che cos'è un database?",
    "Che cos'è il cloud?",
]

for domanda in domande:
    print("Domanda:", domanda)
    print("Senza istruzione:", chiedi(domanda))
    print("Con istruzione:", chiedi(domanda, istruzione))
    print("-" * 30)
