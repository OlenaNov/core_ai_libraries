# Traccia. Scrivi la pipeline come lista di fasi (nome e funzione)
#  e applicala a un testo, stampando a ogni passaggio il tipo e 
# la lunghezza del risultato.
# Alla fine stampa la dimensione di un vettore e quante chiamate 
# sono state fatte.


from initial import *

fasi = [
    ("normalizzazione", normalizza),
    ("chunking", dividi),
    ("embedding", vettorizza)
]

dato = "Il reso è gratuito.\nIl prodotto deve essere integro."
print("ingresso".ljust(16), type(dato).__name__, len(dato))

for nome, funzione in fasi:
    dato = funzione(dato)
    print(nome.ljust(16), type(dato).__name__, len(dato))

    print(len(dato[0]), type(dato[0][0]).__name__)
    print("chiamate a gemini:", chiamate["embedding"])


    #Spiegazione.
# •	FASI è una lista di coppie (nome, funzione). In Python una 
# funzione è un oggetto come gli altri: si può mettere in una 
# lista e chiamare più tardi con funzione(dato).
# •	Il ciclo passa il risultato di ogni fase alla successiva: 
# dato = funzione(dato) sostituisce il dato con l’uscita della 
# fase. Questo è il significato di pipeline.
# •	Ingresso: una stringa di 58 caratteri. Normalizzazione: 
# sempre una stringa, ma di 52 caratteri. Chunking: una lista d
# i 2 frasi. Embedding: una lista di 2 vettori. Il tipo di dato 
# cambia lungo la catena.
# •	Ogni vettore ha 768 numeri decimali (float): la dimensione 
# richiesta a Gemini. Le chiamate sono 2, una per frase: 
# l’embedding è l’unica fase della pipeline che usa l’API.
# Da ricordare. Scrivere le fasi come funzioni separate permette 
# di provarle una alla volta e di sostituirne una senza toccare 
# le altre. Per costo e tempi conta soprattutto la fase che chiama
#  Gemini: il numero di chiamate cresce con il numero di chunk, 
# ed è il motivo per cui il resto della pipeline (registro,
#  impronte, cache) si preoccupa di non rifare le chiamate inutili.
