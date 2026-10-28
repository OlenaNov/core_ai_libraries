
# Chiedi al modello entro quanti giorni arriva il rimborso? prima senza e poi con
# il contesto che contiene la risposta. 

from initial import *


domanda = "Entro quanti giorni arriva il rimborso?"
contesto = "[1] il rimborso arriva entro sette giorni dal ricevimento del reso (fonte: rimborsi.txt)"

prompt_senza = f"domanda: {domanda}"
prompt_con = f"{contesto}\ndomanda: {domanda}"

print(modello_finto(prompt_senza))
print(modello_finto(prompt_con))

