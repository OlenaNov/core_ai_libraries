# metadati_identificativo.py

# Scrivi chunk_ibrido(doc, max_car) che divide per titoli e poi suddivide per frasi solo le sezioni più lunghe di max_car.
# Provala con max_car=300 e max_car=150.
# Spiegazione: è la combinazione consigliata nel modulo: struttura del documento quando c’è, frasi dove una sezione è troppo lunga. 
# Con 300 nessuna sezione supera il limite e i chunk coincidono con le sezioni. 
# Con 150 le prime due sezioni (183 e 178 caratteri) vengono divise in due, e ogni chunk mantiene il titolo della sua sezione.

def chunk_ibrido(doc, max_car):
    risultato = []

    for s in chunk_per_titoli(doc):
        
        if len(s["testo"]) <= max_car:
            parti = [s["testo"]]
        else:
            parti = chunk_frasi(s["testo"], max_car)
        for p in parti:
            risultato.append({"titolo": s["titolo"], "testo": p})
    return risultato

for m in (300, 150):
    c = chunk_ibrido(DOC, m)
    print(m, len(c), [(x["titolo"], len(x["testo"])) for x in c])