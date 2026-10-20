#Traccia: trasforma una frase con spazi doppi o tripli tra le parole in una frase con un solo spazio. 
# Stampa la frase prima e dopo.

testo = "Python    è   un   linguaggio    semplice"

parole = testo.split()
pulito = " ".join(parole)

print("Prima:", testo)
print("Dopo: ", pulito)
