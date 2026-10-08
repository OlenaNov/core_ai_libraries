# Traccia: invia 5 domande a Gemini in due modi, 
# senza istruzione e con l'istruzione "Rispondi sempre in italiano, in una sola frase, come se parlassi a un bambino". Confronta le risposte.

# https://codeshare.io/aJMwAZ
# https://codeshare.io/adQbEM

import time

import httpx
from dotenv import load_dotenv
from google import genai
from google.genai import errors, types

load_dotenv()

client = genai.Client()

MODELLO = "gemini-flash-lite-latest"
TENTATIVI = 5
TIMEOUT_SECONDI = 20
ATTESA_SECONDI = 8


def converti_cronologia(cronologia):
    contenuti = []
    for messaggio in cronologia:
        ruolo = messaggio["role"]
        if ruolo == "assistant":
            ruolo = "model"
        contenuti.append({"role": ruolo, "parts": [{"text": messaggio["content"]}]})
    return contenuti


def chiedi(contenuto, istruzione=None, modello=None):
    if modello is None:
        modello = MODELLO

    if isinstance(contenuto, list):
        contenuto = converti_cronologia(contenuto)

    config = types.GenerateContentConfig(
        system_instruction=istruzione,
        http_options=types.HttpOptions(timeout=TIMEOUT_SECONDI * 1000),
    )

    for tentativo in range(1, TENTATIVI + 1):
        try:
            risposta = client.models.generate_content(
                model=modello,
                contents=contenuto,
                config=config,
            )
            if risposta.text is None:
                return ""
            return risposta.text

        except httpx.TimeoutException:
            if tentativo < TENTATIVI:
                print("  [Timeout di", TIMEOUT_SECONDI, "secondi - riprovo tra", ATTESA_SECONDI, "secondi]")
                time.sleep(ATTESA_SECONDI)
            else:
                print("  [Timeout: nessuna risposta dopo", TENTATIVI, "tentativi]")
                return None

        except errors.APIError as errore:
            if errore.code in (429, 503, 504) and tentativo < TENTATIVI:
                print("  [Servizio occupato, errore", errore.code, "- riprovo tra", ATTESA_SECONDI, "secondi]")
                time.sleep(ATTESA_SECONDI)
            else:
                print("  [Errore", errore.code, ":", errore.message, "]")
                return None

    return None