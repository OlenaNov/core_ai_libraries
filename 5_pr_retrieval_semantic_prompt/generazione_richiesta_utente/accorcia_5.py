
# Scrivi accorcia(testo, max_car) che taglia il testo al massimo 
# a max_car caratteri senza spezzare una parola 
# Provala su una richiesta di 85 caratteri con max_car 40  e su "breve"

def accorcia(testo, max_car):
    if len(testo.strip()) <= max_car:
        return testo
    return testo[:max_car].rsplit(" ", 1)[0]

r = "vorrei sapere come posso restituire un prodotto che ho acquistato la settimana scorsa"

print(len(r))
print(repr(accorcia(r, 40)), len(accorcia(r, 40)))
print(repr(r[:40]))
print(repr(accorcia("breve", 40)))