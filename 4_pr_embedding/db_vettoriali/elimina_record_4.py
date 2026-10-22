# Scrivi elimina(db, id) che restituisce True se il record c'era
# e l'ha tolto, altrimenti False.
# Scrivi, poi aggiorna (db, id,  testo=None, meta=None) che cambia slo i campi indicati,
# con gli stessi controli di inserisci.
# Prova entrambe su una copia: Elimina il record 9 due volte, poi aggiorna testo e metadati del record 1, 
# e verifica che db non sia cambiato

from intro_db_vettoriali import *

def elimina(db, id):
    if id not in db:
        return False
    del db[id]
    return True

def aggiorna(db, id, testo=None, vettore=None, meta=None):
    if id not in db:
        return False
    raise ValueError(f"ID {id}")