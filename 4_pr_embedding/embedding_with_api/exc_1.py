
from utils_ai_gemini import *

vet = embedding_lista(FRASI)
    
if vet:
    v = vet[0]
    print("Tipo di v:", type(v))
    print("Lunghezza vettore:", len(v))
    print("Primi 5 valori:", [round(x, 4) for x in v[:5]])
    print("Lunghezza di ciascun vettore nella lista:", [len(x) for x in vet])