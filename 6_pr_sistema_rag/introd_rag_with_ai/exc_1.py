
# Scrivi genera(prompt) che invia un prompt a Gemini e restform dotenv import load_dotenv(),
# restituisce il testo della risposta. Chiedi la stessa domanda prima senza e poi con il contesto.

from initial import *
from google.genai.errors import ServerError


def genera(prompt):
    try: 
        risposta = client.models.generate_content(model=MODELLO_TESTO, contents=prompt)
        return risposta.text
    except ServerError as e:
        return f"[Errore temporaneo del server: il modello è sovraccarico. Riprova tra poco.]"

prompt_senza = "Domanda:" + domanda
prompt_con = "Contesto:" + contesto + "\nDomanda:" + domanda

print(genera(prompt_senza))
print(genera(prompt_con))