
# Traccia. Calcola l’identificativo di faq/Pagamenti.txt, verifica che percorsi scritti in modo diverso diano lo stesso identificativo e che percorsi diversi no. 
# Calcola l’impronta di un testo, verifica che sia stabile e che cambi con una modifica minima. 
# Mostra che lo stesso testo in un altro percorso ha lo stesso contenuto ma un altro identificativo.


from initial import *

percorso = "faq/Pagamenti.txt"
print(id_documento(percorso))
print(id_documento("FAQ/PAGAMENTI.TXT") == id_documento(percorso))
print(id_documento("faq/altro.txt") == id_documento(percorso))

testo = "Si accertano carta di credito e bonifico bancario"
print(impronta_testo(testo)[:12], len(impronta_testo(testo)))
print(impronta_testo(testo) == impronta_testo(testo))
print(impronta_testo(testo.replace("carta", "carte"))[:12])

copia = "Si accertano carta di credito e bonifico bancario"
print(id_documento("copia/pagamenti.txt") == id_documento(percorso))
print(impronta_testo(copia) == impronta_testo(testo))

