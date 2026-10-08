import time
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client()

MODELS = [
    "gemini-flash-lite-latest",
    "gemini-3.8-flash"
]

TEMPTATIONS = 5

def generate_ai_response(query, instructions):
    for model in MODELS:
        print(
            f"Hi, I'm {model}. I will reply soon."
        )
        timeout_sec = 2

        for temptation in range(1, TEMPTATIONS + 1):
            try:
                print(f"Temptation {temptation}/{TEMPTATIONS}")

                response = client.models.generate_content(
                    model=model,
                    contents=query,
                    config={
                        "system_instruction": instructions,
                        "http_options": {
                            "timeout": 60000
                        }
                    }
                )
                
                return response.text

            except Exception as errore:
                print(f"{type(errore).__name__}: {errore}")

                if temptation < TEMPTATIONS:
                    print(f"I will retry in {timeout_sec} seconds...")

                    time.sleep(timeout_sec)
                    timeout_sec *= 2

                else:
                    print(f"Attempts exhausted for {model}")

        if model != MODELS[-1]: 
            print(f"Model {model} failed. Trying the next model...") 
        
        else: 
            print("No more models available.")

    return (
        "I couldn't answer your question right now. "
        "Please try again later."
    )
