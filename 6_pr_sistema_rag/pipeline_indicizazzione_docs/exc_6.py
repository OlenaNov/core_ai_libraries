
# Scrivi rimuovi_righe_ripetute(pagine, soglia=0.6) che elimina le righe presenti
# # in almeno una certa quota di pagine. Applicala alle tre pagine; poi prova una 
# soglia di 1.0; poi con una terza pagina  che ha un'intestazione diversa, con soglia 
# tra 0.6 e 1.0.


from initial import *

def rimuvi_ridhe_ripetute(pagine, soglia=0.6):
    conteggio = Counter()
    for pagina in pagine:
        for riga in set(pagina.splitlines()):
            conteggio[riga.strip()] += 1
            limite = soglia * len(pagine)
            comuni = {r for r, n in conteggio.items() if n >= limite and r}

    return ["\n".join(r for r in p.splitlines() if r.strip() not in comuni) for p in pagine]

pulite  = rimuvi_ridhe_ripetute(PAGINE)
for p in pulite:
    print(repr(p))
    print([p.splitlines()[0] for p in rimuvi_ridhe_ripetute(altre, 0.6)])
    print([p.splitlines([0] for p in rimuvi_ridhe_ripetute(altre, 1.0))])
            





# Spiegazione.
# •	La funzione conta in quante pagine compare ogni riga: set(pagina.splitlines()) prende le righe senza ripetizioni (così una riga ripetuta due volte nella stessa pagina conta una volta) e conteggio[...] += 1 aggiunge 1.
# •	limite = soglia * len(pagine) è il numero minimo di pagine in cui una riga deve comparire per essere considerata “ripetuta”. Le righe che lo raggiungono (n >= limite) finiscono nell’insieme comuni e vengono tolte da ogni pagina.
# •	Con 3 pagine e soglia 0,6, il limite è 1,8: l’intestazione compare in 3 pagine e viene rimossa. Le righe Pagina 1, Pagina 2... restano, perché sono diverse tra loro: i numeri di pagina richiedono una regola a parte.
# •	Con la soglia 1.0 il limite è 3 pagine su 3: l’intestazione, presente in tutte, viene comunque rimossa.
# •	Nell’ultimo caso l’intestazione compare in 2 pagine su 3. Con soglia 0,6 (limite 1,8) viene rimossa, con soglia 1.0 (limite 3) resta.
