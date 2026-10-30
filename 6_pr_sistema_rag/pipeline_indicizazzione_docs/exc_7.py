# Traccia. Calcola l’identificativo di faq/Pagamenti.txt, verifica che percorsi scritti in 
# modo diverso diano lo stesso identificativo e che percorsi diversi no. Calcola l’impronta di 
# un testo, verifica che sia stabile e che cambi con una modifica minima. Mostra che lo stesso testo in 
# un altro percorso ha lo stesso contenuto ma un altro identificativo.


from initial import *

percorso = "faq/pagamenti.txt"
print(id_documento(percorso))
print(id_documento("FAQ/Pagamenti.TXT") == id_documento(percorso))
print(id_documento("faq/altro.txt") == id_documento(percorso))
testo = "Si accetano carta di credito e bonifico bancario"
print(impronta_testo(testo)[:12], len(impronta_testo(testo)))
print(impronta_testo(testo) == impronta_testo(testo))
print(impronta_testo(testo.replace("carta", "carte"))[:12])

copia = "Si accettano carta di credito e bonifico bancario"
print(id_documento("copia/pagamenti.txt") == id_documento(percorso))
print(impronta_testo(copia) == impronta_testo(testo))




# Spiegazione.
# •	L’identificativo 038e7d92-... è lo stesso su qualsiasi computer, perché dipende solo dallo spazio dei nomi e dal percorso. 
# Scrivere il percorso con maiuscole o spazi diversi dà lo stesso valore (True), un percorso diverso dà un altro valore (False).
# •	L’impronta ha sempre 64 caratteri (qui ne mostriamo 12). 
# Lo stesso testo dà sempre la stessa impronta, e cambiando una parola (carta → carte) l’impronta diventa completamente diversa.
# •	Lo stesso testo conservato in un altro percorso ha un identificativo diverso (False) ma la stessa impronta (True).
