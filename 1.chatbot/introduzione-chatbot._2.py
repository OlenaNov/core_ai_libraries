import time
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client()

MODELLO = "gemini-flash-lite-latest"
TENTATIVI = 5

# Creiamo la sessione di chat che manterrà la memoria dei messaggi
chat = client.chats.create(model=MODELLO)

domande = [
    "Che cos'è Flutter? Rispondi in due righe.",
    "Che cos'è SwiftUI? Rispondi in due righe.",
    "Qual è la differenza tra i due? Rispondi in tre righe.",
    "Quale dei due è meglio per un principiante? Rispondi in due righe.",
    "Riassumi tutto quello che ci siamo detti in una frase.",
]


def invia_con_tentativi(chat, domanda):
    attesa = 2

    for tentativo in range(1, TENTATIVI + 1):
        try:
            # Usiamo chat.send_message per MANTENERE IL CONTESTO della conversazione
            risposta = chat.send_message(
                domanda,
                config={"http_options": {"timeout": 10000}} # Timeout di 10 sec
            )
            return risposta.text

        except Exception as errore:
            print(f"Errore riscontrato ({type(errore).__name__}), tentativo {tentativo} di {TENTATIVI}")
            if tentativo < TENTATIVI:
                print(f"Riprovo tra {attesa} secondi...")
                time.sleep(attesa)
                attesa *= 2  # Raddoppia il tempo di attesa per il tentativo successivo
            else:
                print("Superato il numero massimo di tentativi.")
                return None

    return None


# Ciclo per inviare le domande in sequenza
for i, domanda in enumerate(domande, 1):
    print(f"\n--- Domanda {i}: {domanda} ---")

    testo = invia_con_tentativi(chat, domanda)

    if testo is None:
        print("Non sono riuscito a ottenere la risposta. Mi fermo qui.")
        break
    else:
        print(f"AI: {testo}")