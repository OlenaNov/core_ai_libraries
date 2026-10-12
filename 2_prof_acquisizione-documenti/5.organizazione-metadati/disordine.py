#Traccia: scrivi la funzione problemi_nome(nome) che elenca i difetti di un nome di file (spazi, parentesi, maiuscole, parole ambigue come "finale" o "nuovo", numero finale ambiguo, data ISO o versione mancanti). 
# Applicala ai quattro nomi della dispensa più uno corretto e stampa quanti nomi sono privi di difetti.

import re
from pathlib import Path

PAROLE_AMBIGUE = ["finale", "definitivo", "nuovo", "copia", "ultimo", "vecchio"]


def problemi_nome(nome):
    problemi = []
    stem = Path(nome).stem

    if " " in stem:
        problemi.append("contiene spazi")
    if "(" in stem or ")" in stem:
        problemi.append("contiene parentesi")
    if stem != stem.lower():
        problemi.append("contiene maiuscole")

    for parola in PAROLE_AMBIGUE:
        if parola in stem.lower():
            problemi.append("parola ambigua: " + parola)

    if re.search(r" \d+$", stem):
        problemi.append("numero finale ambiguo (è una versione?)")
    if not re.match(r"^\d{4}-\d{2}-\d{2}", stem):
        problemi.append("manca la data ISO all'inizio")
    if not re.search(r"_v\d+", stem):
        problemi.append("manca la versione (_vN)")

    return problemi


nomi = [
    "manuale utente FINALE (nuovo).txt",
    "preventivo rossi.txt",
    "preventivo rossi copia.txt",
    "preventivo rossi 2.txt",
    "2025-03-14_fattura_rossi-srl_v2.txt",
]

senza_difetti = 0

for nome in nomi:
    problemi = problemi_nome(nome)
    print(nome)

    if len(problemi) == 0:
        print("  nessun difetto")
        senza_difetti = senza_difetti + 1
    else:
        for problema in problemi:
            print("  -", problema)

print()
print("Nomi senza difetti:", senza_difetti, "su", len(nomi))
