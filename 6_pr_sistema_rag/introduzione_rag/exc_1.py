
# Ragruppa i passi nelle due fasi (indicizzazione e interogazzione) e stampali numerati.

from initial import PASSI

FASI = {
    "una volta": [],
    "a ogni domanda": []
}

for passo, quando in PASSI:

    FASI[quando].append(passo)
    NOMI = {
            "una volta": "INDICIZZAZIONE(offline)",
            "a ogni domanda": "INTERROGAZIONE(online)"
        }
    
for quando, passi in FASI.items():
    print(f"{NOMI[quando]} - {len(passi)} passi")
    for numero, passo in enumerate(passi, start=1):
        print(f" {numero} {passo}")