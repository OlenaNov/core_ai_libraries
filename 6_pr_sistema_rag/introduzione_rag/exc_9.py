# Traccia. Scrivi costruisci_prompt(domanda, contesto) che 
# compone il prompt: istruzione, contesto e domanda. 
# Stampalo e mostra la sua lunghezza (caratteri e token stimati) 
# e il numero di a capo.

from initial import *

def costruisci_prompt(domanda, contesto):
    return ("Rispondi usando solo il contesto. Se l'informazione non c'è, rispondi \"Non lo so\".\n\n"
        "Contesto:\n" + contesto + "\n\n"
        "Domanda:" + domanda)

prompt = costruisci_prompt(domanda, contesto)
print(prompt)
print()
print(len(prompt), "caratteri, circa",
      round(len(prompt) / 4), "token")
print(prompt.count("\n"), "a capo")