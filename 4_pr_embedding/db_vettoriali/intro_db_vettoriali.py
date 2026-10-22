
#Esercizio 1: il record e l’archivio
#Traccia. Costruisci l’archivio db: un dizionario che associa a ogni id il suo record, partendo da DOCUMENTI. 
# Stampa quanti record contiene, i campi del primo record, la dimensione del suo vettore, 
# e il testo con vettore e metadati del record 1.

#Spiegazione.
#db = {} crea un dizionario vuoto. Il ciclo prende un record alla volta e lo inserisce con db[d["id"]] = ...: la chiave è l’identificativo, il valore è il record.
#dict(d) crea una copia del record, così modifiche successive ad db non toccano la lista DOCUMENTI. È una copia superficiale: il vettore e i metadati restano condivisi, ma non li modificheremo mai “sul posto”.
#db[1].keys() mostra i campi del record 1: id, testo, vettore, meta. len(db[1]["vettore"]) conferma che il vettore ha 3 numeri.
#Si usa un dizionario per id e non una lista perché permette di trovare un record per identificativo senza scorrere tutto l’archivio (esercizio 3).
#Da ricordare. Un record di un database vettoriale ha sempre le stesse parti: un identificativo, un contenuto (qui il testo), un vettore e dei metadati.

from preparazione_1 import*
db = {}

for d in DOCUMENTI:
    db[d["id"]] = dict(d)

print(len(db))
print(list(db[1].keys()))
print(len(db[1]["vettore"]))
print(db[1]["testo"], db[1]["vettore"], db[1]["meta"])

