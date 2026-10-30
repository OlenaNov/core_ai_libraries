
# Traccia. Estrai i metadati dai due documenti e stampali con il 
# corpo. Scrivi campi_mancanti(metadati) che elenca i campi obbligatori assenti. 
# Prova anche un documento di una sola riga.

from initial import *

def campi_mancanti(metadati):
    return [c for c in OBBLIGATORI if not metadati.get(c)]

for testo in (RESI, BOZZA):
    titolo, riga, corpo = separa_intestazione(testo)
    metadati = estari_metadati(titolo, riga)
    print(metadati, "I mancati:", campi_mancanti(metadati))
    print("corpo:", corpo)

try:
    separa_intestazione("solo titolo")
except ValueError as e:
    print(f"Errore: {e}")


#    SPIEGAZIONE

# •	In RESI la data 03/10/2026 diventa 2026-10-03 (formato ISO: ordina correttamente anche come testo) e la versione è 2.1.
# •	In BOZZA la riga non contiene né data né versione: i due campi valgono None. campi_mancanti usa metadati.get(c) (che restituisce None se la chiave manca) e not per scoprire quali campi obbligatori sono vuoti: risulta mancante data.
# •	Il documento di una sola riga non ha un’intestazione: la funzione solleva un errore, e non si va avanti con dati inventati.
# •	Le espressioni regolari sono deterministiche: con lo stesso testo danno sempre lo stesso risultato. Funzionano su testi con struttura fissa (moduli, schede), non su testi liberi.
# Da ricordare. I metadati (titolo, data, versione) servono a filtrare le ricerche e a citare le fonti. Vanno validati prima di fare il lavoro costoso (chunk ed embedding): un documento con metadati obbligatori mancanti si segnala e si salta, invece di finire nell’indice con dati incompleti.
