# Traccia: crea l'assistente virtuale di una libreria con un'istruzione che ne definisce 
# lo scopo e il tono. Inviagli 6 messaggi, di cui 2 fuori tema, e osserva come reagisce.

from gemini_utils import chiedi

system_instruction = (
    "Sei l'assistente virtuale cordiale e competente di una libreria. "
    "Il tuo scopo è consigliare libri, informare su disponibilità, orari "
    "ed eventi letterari, mantenendo sempre un tono accogliente, "
    "professionale e appassionato di lettura."
)

test_messages = [
    "Avete l'ultimo romanzo di Ken Follett disponibile in negozio?",
    "Mi consiglieresti un buon libro thriller da leggere questo fine settimana?",
    "A che ora chiudete la libreria questa sera?",
    "Ci saranno presentazioni di libri o eventi con autori nei prossimi giorni?",
    "Sai dirmi che tempo farà domani a Milano?",
    "Qual è la ricetta migliore per preparare la carbonara?"
]

for message in test_messages:
    print(f"Domanda: {message}")
    print(f"Response: {chiedi(message, system_instruction)}")