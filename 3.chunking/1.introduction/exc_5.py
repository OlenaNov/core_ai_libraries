# TODO  

#Scrivi chunk_frasi(testo, max_car) che aggiunge frasi intere a un chunk finché non supererebbe max_car caratteri.
# Provala con max_car=200.
#Spiegazione: la variabile corrente contiene il chunk in costruzione.
# Per ogni frase si controlla se aggiungerla (più 1 per lo spazio) supererebbe il limite: in quel caso si chiude il chunk e si riparte dalla frase;
# altrimenti la si accoda. Dopo il ciclo va salvato anche l’ultimo chunk. Nessuna frase viene spezzata, ma le lunghezze sono irregolari (186 e 153).

