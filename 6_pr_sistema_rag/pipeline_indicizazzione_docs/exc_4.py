
# Traccia. Verifica che "caffè" scritto in forma composta e 
# scomposta sia considerato lo stesso testo solo dopo la 
# normalizzazione. 
# Normalizza un testo con spazi e a capo irregolari. Poi confronta
#  le impronte (SHA-256, abbreviate) dei due testi prima e dopo.

from initial import *

composta = "caffé"
scomposta = unicodedata.normalize("NFD", composta)
print(len(composta), len(scomposta), scomposta == composta)
print(normalizza_testo(composta) == normalizza_testo(scomposta))

grezzo = "IL reso è\r\ngratuito\n\n\nil prodotto\tdeve essere integro."
print(repr(normalizza_testo(grezzo)))

def impronta(testo):
    return hashlib.sha256(testo.encode("utf-8")).hexdigest()[:12]

print(impronta(composta) == impronta(scomposta))
print(impronta(normalizza_testo(composta)) == impronta(normalizza_testo(scomposta)))