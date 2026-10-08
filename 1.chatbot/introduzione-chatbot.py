import time
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client()

modelli = ["gemini-3.8-flash", "gemini-flash-lite-latest"]
tentativi_per_modello = 4
domanda = "Che cos'è Flutter? Rispondi in due righe."

print("Domanda inviata:", repr(domanda))

def chiedi(domanda):
    for modello in modelli:
        print(f"\n---> Provo con il modello: {modello}")
        attesa = 2
        for tentativo in range(1, tentativi_per_modello + 1):
            try:
                print(f"Tentativo {tentativo}/{tentativi_per_modello} su {modello}...")
                
                # Impostiamo un timeout di 10 secondi per evitare blocchi infiniti
                risposta = client.models.generate_content(
                    model=modello,
                    contents=domanda,
                    config={"http_options": {"timeout": 10000}} # 10000 ms = 10 sec
                )
                return risposta.text
                
            except Exception as errore:
                # Stampiamo L'ERRORE REALE per capire perché fallisce
                print(f"Errore riscontrato ({type(errore).__name__}): {errore}")
                
                # Se è un errore di rate limit o server occupato, riproviamo
                print(f"Riprovo tra {attesa} secondi...")
                time.sleep(attesa)
                attesa *= 2

    return "Nessun modello ha risposto. Riprova più tardi."

print("\nRisultato AI:", chiedi(domanda))