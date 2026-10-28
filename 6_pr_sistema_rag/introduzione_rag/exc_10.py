
# Il modello può ricevere un numero limitato di token. Scrivi 
# entra_nel_budget(risultati, max_token) che tiene i chunk, dal più simile,
# finché la loro somma di token stimati non supera max_token,
# e restituisce i chunk scelti e i token usati. Provala con budget 100, 35 e 10
# sui 4 risultati di "Entro quanti giorni arriva il rimborso?".


from initial import *

def stima_token(testo):
    return round(len(testo) / 4)

def entra_nel_budget(risultati, max_token):
    scelti = []
    usati = 0
    for punteggio, chunk in risultati:
        costo = stima_token(chunk["testo"])
        if usati + costo > max_token:
            break
        scelti.append((punteggio, chunk))
        usati += costo
    return (scelti, usati)

risultati = cerca("Entro quanti giorni arriva il rimborso?", indice, 4)
print([(round(p, 2), c["id"], stima_token(c["testo"])) for p, c in risultati])

for budget in (100, 35, 10):
    scelti, usati = entra_nel_budget(risultati, budget)
    print(budget, "->", [c["id"] for p, c in scelti], usati)