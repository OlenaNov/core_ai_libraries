# Leggere un record per id
# Scrivi leggi(db, id) che ristituisce il record con quell'id
# oppure None se non esiste.
# Leggi il record 4 e il 99, poi ricupera i testi del record
# 1, 5, e 99 ignorando quelli mancati

from preparazione_1 import *
from intro_db_vettoriali import *

def leggi(dd, id):
    return db.get(id)

print(leggi(db, 4)["testo"])
print(leggi(db, 7))
print([leggi(db, i)["testo"] for i in (1,5,7) if leggi(db, i) is not None])