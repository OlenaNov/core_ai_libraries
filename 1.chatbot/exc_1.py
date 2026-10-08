# Traccia: invia a Gemini una domanda scritta nel codice e stampa la risposta. Se qualcosa va storto, stampa un messaggio di errore al posto di far chiudere il programma.

import time

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()

MODELLI = [
    "gemini-flash-lite-latest",
    "gemini-3.8-flash"
    
]

TENTATIVI = 5

domanda = input("Tu: ").strip()


def chiedi(domanda):

    for modello in MODELLI:

        print(
            f"Ciao, mi chiamo {modello}, "
            "ti rispondo il prima possibile"
        )

        attesa = 2

        for tentativo in range(1, TENTATIVI + 1):

            try:

                print(
                    f"Tentativo {tentativo}/{TENTATIVI}"
                )

                risposta = client.models.generate_content(
                    model=modello,
                    contents=domanda,
                    config={
                        "http_options": {
                            "timeout": 60000
                        }
                    }
                )

                return risposta.text

            except Exception as errore:

                print(
                    f"{type(errore).__name__}: {errore}"
                )

                if tentativo < TENTATIVI:

                    print(
                        f"Riprovo tra {attesa} secondi..."
                    )

                    time.sleep(attesa)

                    attesa *= 2

                else:

                    print(
                        f"Tentativi esauriti per {modello}."
                    )

        print(
            f"Passo al modello successivo: "
            f"{MODELLI[MODELLI.index(modello) + 1]}"
            if modello != MODELLI[-1]
            else "Nessun altro modello disponibile."
        )

    return (
        "Non sono riuscito a risponderti adesso, "
        "prova, per favore, più tardi."
    )


print(f"\nRisposta: {chiedi(domanda)}")