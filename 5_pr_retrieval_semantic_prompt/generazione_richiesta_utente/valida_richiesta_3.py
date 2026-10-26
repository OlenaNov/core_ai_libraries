
# Scrivi valida_richiesta(testo, minimo=3, massimo=500),
# che che solleva un ValueError con un messaggio chiaro
# se la richiesta è vuota, più corta del minimo o più lunga del massimo

from pulisci_richiesta_2 import pulisci_richiesta


def valida_richiesta(testo, min=3, max=500):
    if not testo:
        raise ValueError("La richiesta è vuota.")
    if len(testo.strip()) < min:
        raise ValueError(f"La richiesta è troppo corta, deve avere almeno {min} caratteri.")
    if len(testo.strip()) > max:
        raise ValueError(f"La richiesta è troppo lunga, deve avere una lunghezza massima di {max} caratteri.")
    return testo


def main() -> None:
    testi = ["", "ok", "L'intelligenza artificiale moderna rappresenta una delle rivoluzioni tecnologiche più profonde della storia umana, capace di trasformare radicalmente il modo in cui elaboriamo i dati, risolviamo problemi complessi e automatizziamo processi industriali e creativi; grazie ai progressi strabilianti nel campo del machine learning, delle reti neurali profonde, dei modelli linguistici di grandi dimensioni e dell'architettura transformer, i sistemi intelligenti odierni non si limitano più a eseguire rigide istruzioni programmate, ma sono in grado di apprendere autonomamente dai dati, comprendere il linguaggio naturale con sfumature simili a quelle umane, generare contenuti multimediali originali, analizzare immagini mediche con precisione millimetrica e persino supportare i programmatori nello sviluppo del software attraverso la generazione di codice e il debugging predittivo, aprendo scenari etici, filosofici ed economici senza precedenti che richiedono una regolamentazione attenta, una costante supervisione umana e un impegno etico collettivo volto a garantire che lo sviluppo tecnologico rimanga sempre al servizio del benessere e del progresso dell'intera umanità, riducendo le disuguaglianze e promuovendo la trasparenza e la sicurezza dei sistemi autonomi in ogni settore della società contemporanea.", "Come posso pagare?"]

    for testo in testi:
        try:
            print(repr(valida_richiesta(pulisci_richiesta(testo))))

        except ValueError as e:
            print(f"Errore {e}")

if __name__ == "__main__":
    main()