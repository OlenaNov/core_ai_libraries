#Traccia: hai 6 documenti, ciascuno con un testo e alcuni metadati (nome del file, tipo, controparte, data). 
# Stampa per ognuno che cosa dice il testo e che cosa dicono i metadati. 
# Poi, senza leggere i testi, trova le fatture di rossi-srl emesse dal 1° gennaio 2025 e conta i documenti per tipo.

documenti = [
    {
        "file": "2024-11-02_contratto_verdi-spa_v1.txt",
        "tipo": "contratto",
        "controparte": "verdi-spa",
        "data": "2024-11-02",
        "testo": "Contratto di fornitura con Verdi SpA, durata 24 mesi.",
    },
    {
        "file": "2025-01-20_fattura_rossi-srl_v1.txt",
        "tipo": "fattura",
        "controparte": "rossi-srl",
        "data": "2025-01-20",
        "testo": "Fattura 12/2025 a Rossi Srl: totale 800,00 euro.",
    },
    {
        "file": "2025-03-14_fattura_rossi-srl_v2.txt",
        "tipo": "fattura",
        "controparte": "rossi-srl",
        "data": "2025-03-14",
        "testo": "Fattura 41/2025 a Rossi Srl: totale 1.250,00 euro.",
    },
    {
        "file": "2025-02-11_fattura_bianchi-snc_v1.txt",
        "tipo": "fattura",
        "controparte": "bianchi-snc",
        "data": "2025-02-11",
        "testo": "Fattura 25/2025 a Bianchi Snc: totale 300,00 euro.",
    },
    {
        "file": "2024-12-05_preventivo_rossi-srl_v1.txt",
        "tipo": "preventivo",
        "controparte": "rossi-srl",
        "data": "2024-12-05",
        "testo": "Preventivo per Rossi Srl: totale 2.000,00 euro.",
    },
    {
        "file": "2024-12-01_manuale_interno_v1.txt",
        "tipo": "manuale",
        "controparte": "",
        "data": "2024-12-01",
        "testo": "Manuale utente: premere il pulsante per accendere il dispositivo.",
    },
]

print("--- Testo e metadati ---")
for d in documenti:
    print("Il testo dice:     ", d["testo"])
    print("I metadati dicono: ", d["tipo"], "|", d["controparte"], "|", d["data"])
    print()

print("--- Fatture di rossi-srl dal 2025-01-01 ---")
for d in documenti:
    if d["tipo"] == "fattura" and d["controparte"] == "rossi-srl" and d["data"] >= "2025-01-01":
        print(d["file"])

print()
print("--- Documenti per tipo ---")
conteggio = {}
for d in documenti:
    tipo = d["tipo"]
    if tipo in conteggio:
        conteggio[tipo] = conteggio[tipo] + 1
    else:
        conteggio[tipo] = 1

for tipo, numero in conteggio.items():
    print(tipo, ":", numero)
