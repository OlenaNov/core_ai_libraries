
# Scrivi pulisci richiesta(testo) che toglie gli spazzi
# in eccesso gli a capo e gli spazzi a bordi.
# Provala su "Come posso\n restituire un prodotto?"
# e su " "


def pulisci_richiesta(testo):
    return " ".join(testo.split())

def main() -> None:
    testo1 = "Come posso\n restituire un prodotto?"
    testo2 = " "

    print(repr(pulisci_richiesta(testo1)))
    print(repr(pulisci_richiesta(testo2)))

if __name__ == "__main__":
    main()