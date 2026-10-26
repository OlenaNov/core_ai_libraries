# Un modello accetta un numero massimo di token in ingresso: supponiamo 512
# con la stima di un token ogni 4 caratteri.
# Scrivi entra_nel_limite(testo, limite=512)

LIMITE_TOKEN = 512

def stima_token(testo):
    return round(len(testo) / 4)


def entra_nel_limite(testo: str, limite: int=LIMITE_TOKEN):
    return stima_token(testo) <= limite


def main() -> None:
    testi = ["parola"*400, "Come posso pagare?"]

    for testo in testi:
        print(len(testo), stima_token(testo), entra_nel_limite(testo))

if __name__ == "__main__":
    main()