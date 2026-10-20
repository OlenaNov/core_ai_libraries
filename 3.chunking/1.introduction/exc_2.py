# TODO exc2

#Scrivi n_attesi(lunghezza, dim, overlap) che calcola con una formula quanti chunk si ottengono,
# e verifica che coincida con chunk_caratteri per tre combinazioni di parametri.
#Spiegazione: i chunk partono ogni passo caratteri,
# quindi il loro numero è lunghezza / passo arrotondato per eccesso (math.ceil).
# Con 340 caratteri e passo 80 si ha 340 / 80 = 4,25, quindi 5 chunk.
# Saper prevedere il numero di chunk serve a stimare in anticipo costi e dimensione dell’indice.

