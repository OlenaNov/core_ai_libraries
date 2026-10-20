#Scrivi chunk_parole(test, dim, overlap=0) in cui dim e overlap sono espressi in parole.
# Provala con dim=12 e overlap=3.
#Spiegazione: si lavora sulla lista delle parole (split()) e si ricompone ogni blocco con " ".join(...).
# Le parole restano intere, e le 3 parole in comune tra chunk consecutivi si vedono (dalla consegna. La, Le spese di...).
# Il break interrompe il ciclo quando il blocco ha raggiunto la fine del testo, per non creare blocchi inutili.
# I tagli però cadono comunque a metà frase (“...consegna. La” / “richiesta”).

from utils import *

def chunk_parole(test, dim, overlap=0):
    parole = test.split()
    passo = dim -overlap
    risultato = []

    for i in range(0, len(parole), passo):
        blocco = parole[i:i + dim]
        risultato.append(" ".join(blocco))
        if i + dim >= len(parole):
            break

    return risultato

c = chunk_parole(TEXT, 12, 3)
print(f"{len(c)} chunk")
for x in c:
    print(x)