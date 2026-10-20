# TODO exc1


#Scrivi chunk_caratteri(testo, dim, overlap=0) che taglia il testo in chunk di dim caratteri, 
# facendo ripartire ogni chunk overlap caratteri prima della fine del precedente. 
# Provala con dim=100 e overlap 0 e 20.


#Spiegazione: il passo è dim - overlap: senza overlap vale 100, 
# con overlap 20 vale 80. range(0, len(testo), 
# passo) genera le posizioni di partenza e lo slice testo[i:i + dim] taglia il pezzo.
# L’ultimo chunk è più corto perché il testo finisce. 
# Gli ultimi 20 caratteri del primo chunk coincidono con i primi 20 del secondo (a richiesta si invia).
# Nota che con overlap 20 l’ultimo chunk (20 caratteri) ,
# è interamente contenuto nel precedente: è testo ripetuto che non aggiunge nulla.

