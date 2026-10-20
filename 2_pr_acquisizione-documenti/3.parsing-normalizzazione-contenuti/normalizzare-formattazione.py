#Traccia: il testo contiene a capo di tipo diverso (\r\n di Windows, \r del vecchio Mac, \n) e righe vuote. Rendi uniformi gli a capo, elimina le righe vuote e stampa la lista finale con il numero di righe.

testo = "Riga uno\r\nRiga due\rRiga tre\n\n\nRiga quattro"

testo = testo.replace("\r\n", "\n")
testo = testo.replace("\r", "\n")

righe = []
for riga in testo.split("\n"):
    if riga.strip() != "":
        righe.append(riga.strip())

print(righe)
print("Numero di righe:", len(righe))
