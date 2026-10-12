#Traccia: codifica la lettera "è" in utf-8, latin-1 e utf-16-le e stampa i byte ottenuti con la loro lunghezza. 
# Poi stampa quanti byte occupano in UTF-8 i caratteri A, è, € e 😀. Verifica che "Perché" ha 6 caratteri ma 7 byte. 
# Infine decodifica i byte UTF-8 della "è" in due modi, uno giusto e uno sbagliato.


lettera = "è"

print("--- Una lettera in tre codifiche ---")
for codifica in ["utf-8", "latin-1", "utf-16-le"]:
    dati = lettera.encode(codifica)
    print(codifica, "->", dati, "(", len(dati), "byte )")

print()
print("--- Byte occupati in UTF-8 ---")
for carattere in ["A", "è", "€", "😀"]:
    dati = carattere.encode("utf-8")
    print(carattere, "occupa", len(dati), "byte")

print()
parola = "Perché"
print(parola, ":", len(parola), "caratteri,", len(parola.encode("utf-8")), "byte")

print()
print("--- Decodifica giusta e sbagliata ---")
dati = "è".encode("utf-8")
print("Letta come utf-8:", dati.decode("utf-8"))
print("Letta come latin-1:", dati.decode("latin-1"))
