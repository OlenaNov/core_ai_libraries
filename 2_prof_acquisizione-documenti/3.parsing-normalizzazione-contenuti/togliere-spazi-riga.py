#Traccia: hai un testo con righe che hanno spazi all'inizio e alla fine. 
# Crea una lista di righe pulite e stampale tra parentesi quadre,
# così si vede se gli spazi sono spariti.

testo = "   Prima riga   \n  Seconda riga\nTerza riga   "

righe_pulite = []
for riga in testo.splitlines():
    righe_pulite.append(riga.strip())

for riga in righe_pulite:
    print("[" + riga + "]")
