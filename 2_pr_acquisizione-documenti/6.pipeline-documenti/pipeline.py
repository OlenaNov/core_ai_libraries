def estrai_testo(percorso):
    with open(percorso, encoding="utf-8") as f:
        return f.read()

def normalizza(testo):
    return " ".join(testo.split())

FASI = [estrai_testo, normalizza]

def esegui(percorso, fasi=FASI):
    risultato = percorso
    for fase in fasi:
        risultato = fase(risultato)
    return risultato

print(esegui("a.txt"))

# Sostituire una sola fase, ad esempio con un parser diverso:
def estrai_testo_v2(percorso):
    with open(percorso, encoding="utf-8-sig") as f:   # ignora il BOM
        return f.read()

print(esegui("a.txt", fasi=[estrai_testo_v2, normalizza]))
