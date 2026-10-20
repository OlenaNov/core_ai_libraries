
macchine = {
    "auto": [0.9, 0.1],
    "moto": [0.85, 0.2],
    "furgone": [0.1, 0.9]
}

print(len(macchine["auto"]))
print([len(v) for v in macchine.values()])

def stessa_dimensione(vettori):
    dimensioni = set()
    for v in vettori:
        dimensioni.add(len(v))
    return len(dimensioni) == 1

print(stessa_dimensione([[1,2], [3,4], [5,6]]))
print(stessa_dimensione([[1,2], [3,4,5]]))