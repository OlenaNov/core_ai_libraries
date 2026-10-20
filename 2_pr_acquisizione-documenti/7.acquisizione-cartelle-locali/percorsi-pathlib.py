from pathlib import Path

# (a)
base = Path("documenti_clienti")
file = base / "2025" / "rossi" / "Contratto.PDF"

# (b)
def descrivi(percorso):
    p = Path(percorso)
    return {
        "nome": p.name,
        "stem": p.stem,
        "estensione": p.suffix.lower(),
        "cartella": p.parent.name,
        "esiste": p.exists(),
    }

print(descrivi(file))
# {'nome': 'Contratto.PDF', 'stem': 'Contratto', 'estensione': '.pdf',
#  'cartella': 'rossi', 'esiste': False}

# (c)
Path("output/testi").mkdir(parents=True, exist_ok=True)

# Bonus: stesso percorso con altra estensione
print(file.with_suffix(".txt"))   # documenti_clienti/2025/rossi/Contratto.txt

