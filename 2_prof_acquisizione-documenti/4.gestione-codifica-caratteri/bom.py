#Traccia: stampa i BOM di UTF-8, UTF-16 little endian e UTF-16 big endian. Poi hai un file CSV con il BOM all'inizio: decodificalo come utf-8 e come utf-8-sig, 
# e per ciascuna decodifica stampa l'intestazione della prima riga e controlla se la prima colonna si chiama davvero nome.

import codecs

print("BOM UTF-8:", codecs.BOM_UTF8)
print("BOM UTF-16 little endian:", codecs.BOM_UTF16_LE)
print("BOM UTF-16 big endian:", codecs.BOM_UTF16_BE)
print()

dati = b"\xef\xbb\xbfnome;cognome;importo\nGiuseppe;Rossi;10"

risultati = [
    ("utf-8", dati.decode("utf-8")),
    ("utf-8-sig", dati.decode("utf-8-sig")),
]

for nome_codifica, testo in risultati:
    colonne = testo.split("\n")[0].split(";")
    print("Decodificato con", nome_codifica)
    print("  Colonne:", colonne)
    print("  La prima colonna è 'nome'?", colonne[0] == "nome")
    print("  Lunghezza del nome della prima colonna:", len(colonne[0]))
    print()
