import hashlib
import math
import re
import statistics

test = (
    "Il cliente può restituire il prodotto entro quattordici giorni dalla consegna. "
    "La richiesta si invia dall'area personale. Il rimborso avviene entro sette giorni "
    "dal ricevimento del reso. Le spese di spedizione restano a carico del cliente. "
    "I prodotti personalizzati non si possono restituire. Per ogni dubbio si può contattare l'assistenza."
)

ordine = "L'ordine da lei effettuato è in fase di elaborazione"

nome = "Il sig. Rossi ha pagato 1.234,50 euro. Ha ricevuto il rimborso."

DOC = """# Guida ai resi
## Come richiedere il reso
Il cliente può restituire il prodotto entro quattordici giorni dalla consegna. La richiesta si invia dall'area personale. Il prodotto deve essere integro e nella confezione originale.
## Rimborso
Il rimborso avviene entro sette giorni dal ricevimento del reso. Le spese di spedizione restano a carico del cliente. Il rimborso usa lo stesso metodo di pagamento dell'acquisto.
## Eccezioni
I prodotti personalizzati non si possono restituire."""