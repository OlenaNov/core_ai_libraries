#  Traccia. Scrivi recupera(domanda, indice, k=2, soglia=0.2) che 
# scarta i risultati con punteggio sotto la soglia.
#  Provala con "Quanto costa la spedizione?" e con la domanda fuori
#  argomento "Che tempo fa oggi?", mostrando anche i risultati 
# senza soglia.
 


from initial import *

def recupera(domanda, indice, k=2, soglia=0.2):
    return [r for r in cerca(domanda, indice, k) if r[0] >= soglia]

for domanda in (
    "Quanto costa la spedizione?",
    "Che tempo fa oggi?"
):
   trovati = recupera(domanda, indice)
   print(f"Domanda -> {[(round(p, 2), c["id"]) for p, c in trovati]}") 
   print(f"Senza soglia: -> {[(round(p, 2), c["id"]) for p, c in cerca(domanda, indice, 4)]}") 
