# Scrivi cerca(domanda, indice, k=2) che calcola la somiglianza tra la 
# domanda e ogni chunk con il prodotto scalare e restituisce i 
# k migliori come coppie (punteggio, chunk). 
# Provala con due domande, chiedendo 3 risultati.


from initial import *

def cerca(domanda, indice, k=2):
    q = embedding_domanda(domanda)
    risultati = []

    for d in indice:
        punteggio = sum(a * b for a, b in zip(q, d["vettore"]))
        risultati.append((punteggio, d))

    risultati.sort(key=lambda x: x[0], reverse=True)
    return risultati[:k]

for domanda in (
    "Quanto costa la spedizione?",
    "Entro quanti giorni arriva il rimborso?"
):
    print(domanda)
    for punteggio, chunk in cerca(domanda, indice, 3):
        print(f"{round(punteggio, 2)} {chunk["id"]} {chunk["fonte"]}")

