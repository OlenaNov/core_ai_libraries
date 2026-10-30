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
print("scartati: ", scartati)
print(len(elenca_file(cartella, ".md")))