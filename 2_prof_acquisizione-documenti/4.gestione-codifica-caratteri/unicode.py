#Traccia: per i caratteri A, è, ù, € e 😀 stampa il punto di codice in esadecimale, 
# nella forma U+... e con il nome Unicode. Poi fai il percorso inverso, da punto di codice a carattere. 
# Infine stampa i punti di codice di ogni lettera della parola "città".

import unicodedata

print("--- Dal carattere al punto di codice ---")
for carattere in ["A", "è", "ù", "€", "😀"]:
    punto = ord(carattere)
    forma_unicode = "U+" + format(punto, "04X")
    print(carattere, "|", hex(punto), "|", forma_unicode, "|", unicodedata.name(carattere))

print()
print("--- Dal punto di codice al carattere ---")
for punto in [0x41, 0xE8, 0x20AC, 0x1F600]:
    print(hex(punto), "->", chr(punto))

print()
print("--- Le lettere di 'città' ---")
for carattere in "città":
    print(carattere, "U+" + format(ord(carattere), "04X"))
