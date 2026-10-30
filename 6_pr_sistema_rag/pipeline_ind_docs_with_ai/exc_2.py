
# Traccia. Elenca i file ammessi stampando il percorso relativo e 
# la dimensione in byte, poi i file scartati. Prova anche a 
# limitare l’elenco ai file .md.

from initial import *

tutti = [p for p in cartella.rglob("*") if p.is_file()]
accettati = elenca_file(cartella)
print(len(tutti), "file in totale")

for p in accettati:
    print(p.relative_to(cartella).as_posix().ljust(20), p.stat().st_size, "byte")

scartati = sorted(p.name for p in tutti if p not in accettati)
print("scartati:", scartati)
print(len(elenca_file(cartella, (".md"))))



# Spiegazione.
# •	tutti raccoglie tutti i file della cartella (5), accettati solo quelli con estensione ammessa (4).
# •	p.relative_to(cartella).as_posix() dà il percorso relativo alla cartella, con le barre /: è un identificativo stabile (il percorso assoluto cambia da computer a computer,
# quello relativo no). p.stat().st_size è la dimensione in byte, non in caratteri: una lettera accentata come è occupa 2 byte in UTF-8.
# •	scartati contiene i file non ammessi: logo.png. Limitando le estensioni a (".md",) resta un solo file.
