import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(
    http_options=types.HttpOptions(timeout=60000)  
)

domanda = "Che cos'è un chatbot? Rispondi in due righe."
print("Domanda:", domanda)

MAX_TENTATIVI = 6
ATTESA_BASE = 8  

chat = client.chats.create(model="gemini-flash-lite-latest")

for tentativo in range(1, MAX_TENTATIVI + 1):
    try:
        print(f"Tentativo {tentativo}/{MAX_TENTATIVI}...")
        risposta = chat.send_message(domanda)
        print("AI:", risposta.text)
        break
    except Exception as errore:
        print(f"Errore (tentativo {tentativo}/{MAX_TENTATIVI}):", errore)
        if tentativo < MAX_TENTATIVI:
            attesa = ATTESA_BASE * tentativo
            print(f"Riprovo tra {attesa} secondi...")
            time.sleep(attesa)
        else:
            print("Numero massimo di tentativi raggiunto. Operazione fallita.")