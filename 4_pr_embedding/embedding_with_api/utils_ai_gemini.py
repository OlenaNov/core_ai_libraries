import os
import time
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

MODELLO = "gemini-embedding-001" 

FRASI = [
    "il gatto dorme sul divano",
    "il cane dorme sul tappeto",
    "la mela è un frutto dolce",
    "la pera è un frutto dolce",
    "il cane corre nel parco",
    "mangio una mela rossa",
]

def embedding_lista(testi, compito=None, dimensione=None):
    """Genera gli embedding reali chiamando l'API di Gemini con gestione dei tentativi."""
    config = types.EmbedContentConfig(task_type=compito, output_dimensionality=dimensione) if (compito or dimensione) else None

    for n in range(3):
        try:
            risposta = client.models.embed_content(
                model=MODELLO, 
                contents=testi, 
                config=config
            )
            return [e.values for e in risposta.embeddings]
        except Exception as e:
            print(f"Errore: {e}. Nuovo tentativo in corso...")
            if n == 2:
                raise
            time.sleep(2)

def stessa_dimensione(vettori):
    """Verifica se tutti i vettori passati hanno esattamente la stessa dimensione."""
    dimensioni = set()
    for v in vettori:
        dimensioni.add(len(v))
    return len(dimensioni) == 1


if __name__ == "__main__":
    print("⏳ Generazione degli embedding reali da Gemini in corso...")
    vet = embedding_lista(FRASI)
    print("✅ Embedding generati con successo!\n")
    
    if vet:
        v = vet[0]
        print(f"Tipo di v: {type(v)}")
        print(f"Numero totale di frasi vettorizzate: {len(vet)}")
        print(f"Lunghezza (dimensioni) di ciascun vettore: {[len(x) for x in vet]}")
        print(f"Primi 5 valori del primo vettore: {[round(x, 4) for x in v[:5]]}\n")
        
        print("--- TEST DELLA FUNZIONE STESSA_DIMENSIONE ---")
        print("I vettori generati hanno tutti la stessa dimensione?", stessa_dimensione(vet))
        
        print("Test con dimensione alterata:", stessa_dimensione(vet + [[1, 2, 3]]))