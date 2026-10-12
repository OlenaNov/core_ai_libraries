from gemini_utils import chiedi

istruzione = (
    "Sei l'assistente virtuale di una libreria. "
    "Aiuti i clienti con consigli di lettura e informazioni sui libri. "
    "Rispondi in italiano, in massimo due frasi, con tono cordiale. "
    "Se la domanda non riguarda i libri, spiega gentilmente che non puoi aiutare."
)

messaggi = [
    "Avete libri di cucina?",
    "Mi consigli un romanzo giallo?",
    "Cerco un libro per una bambina di cinque anni.",
    "Come si fa la carbonara?",
    "Che tempo farà domani?",
    "Mi consigli un classico della letteratura italiana?",
]

for messaggio in messaggi:
    print("Cliente:", messaggio)
    print("Bot:", chiedi(messaggio, istruzione))
    print("-" * 30)
