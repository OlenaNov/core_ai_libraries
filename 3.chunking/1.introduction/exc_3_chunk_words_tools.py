# TODO dal esempio del prof collegando chat bot per fornire il testo
#Scrivi chunk_parole(test, dim, overlap=0) in cui dim e overlap sono espressi in parole.
# Provala con dim=12 e overlap=3.
#Spiegazione: si lavora sulla lista delle parole (split()) e si ricompone ogni blocco con " ".join(...).
# Le parole restano intere, e le 3 parole in comune tra chunk consecutivi si vedono (dalla consegna. La, Le spese di...).
# Il break interrompe il ciclo quando il blocco ha raggiunto la fine del testo, per non creare blocchi inutili.
# I tagli però cadono comunque a metà frase (“...consegna. La” / “richiesta”).
# Crea un report per tutti i tools creati, indicando: azione, date, resultato ..


