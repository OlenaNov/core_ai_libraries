
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors


load_dotenv()

client = genai.Client()

MODELLI = [
    "gemini-3.8-flash",
    "gemini-flash-lite-latest",
]

TENTATIVI = 4

domande = [
    "Che cos'è Flutter? Rispondi in due righe.",
    "Che cos'è SwiftUI? Rispondi in due righe.",
    "Qual è la differenza tra i due? Rispondi in tre righe.",
    "Quale dei due è meglio per un principiante? Rispondi in due righe.",
    "Riassumi tutto quello che ci siamo detti in una frase.",
]


def invia_con_tentativi(domanda):

    for modello in MODELLI:

        print()
        print("=" * 50)
        print("Provo con il modello:", modello)
        print("=" * 50)

        attesa = 2

        for tentativo in range(1, TENTATIVI + 1):

            try:
                print(
                    f"Tentativo {tentativo}/{TENTATIVI} "
                    f"su {modello}..."
                )

                risposta = client.models.generate_content(
                    model=modello,
                    contents=domanda,
                )

                return risposta.text

            except errors.APIError as errore:

                # ------------------------------------------------
                # 404 = modello non disponibile
                # Passiamo direttamente al modello successivo
                # ------------------------------------------------

                if errore.code == 404:

                    print(
                        "Modello",
                        modello,
                        "non disponibile."
                    )

                    break

                # ------------------------------------------------
                # 429 = quota/rate limit
                # Passiamo al modello successivo
                # ------------------------------------------------

                elif errore.code == 429:

                    print(
                        "Quota/rate limit raggiunto per",
                        modello
                    )

                    print(
                        "Passo al modello successivo..."
                    )

                    break

                # ------------------------------------------------
                # 503 = server temporaneamente occupato
                # Possiamo fare retry
                # ------------------------------------------------

                elif errore.code == 503:

                    print(
                        "Server temporaneamente occupato.",
                        f"Tentativo {tentativo}/{TENTATIVI}"
                    )

                    if tentativo < TENTATIVI:

                        print(
                            f"Riprovo tra {attesa} secondi..."
                        )

                        time.sleep(attesa)

                        attesa *= 2

                    else:

                        print(
                            "Tentativi esauriti."
                        )

                # ------------------------------------------------
                # Altri errori
                # ------------------------------------------------

                else:

                    print(
                        "Errore API:",
                        errore.code,
                        errore.message
                    )

                    return None

    return None


# ============================================================
# CICLO PRINCIPALE
# ============================================================

for numero, domanda in enumerate(domande, start=1):

    print()
    print("Domanda", numero)
    print("-" * 50)
    print(domanda)

    testo = invia_con_tentativi(domanda)

    if testo is None:

        print()
        print(
            "Nessun modello è riuscito a rispondere."
        )

        break

    print()
    print("AI:", testo)
    print("-" * 50)

