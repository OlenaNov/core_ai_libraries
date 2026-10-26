
# Che cosa fa la preparazione
# A che cosa serve. Gli esercizi chiamano client.models.embed_content(...), come si fa con Gemini. 
# La preparazione fornisce un client simulato che risponde allo stesso modo, così puoi provare tutto offline. Dopo gli import ci sono quattro blocchi.
# 1. Gli import.
# •	hashlib fornisce md5, una funzione che trasforma un testo in un numero sempre uguale per lo stesso testo.
# •	math serve per la radice quadrata (math.sqrt).
# •	re fornisce le espressioni regolari, usate per dividere il testo in parole.
# •	SimpleNamespace è un contenitore semplice: permette di creare un oggetto con degli attributi, come risposta.embeddings, senza scrivere una classe.
# 2. La funzione _vettore(testo, dim, normalizza) produce il vettore simulato di un testo.
# •	La prima riga (re.sub) toglie un eventuale prefisso del tipo task: ... | query: oppure title: ... | text:: il simulato non ha un modello che capisca le istruzioni, 
# quindi le ignora. Con Gemini vero il prefisso conta.
# •	v = [0.0] * dim crea un vettore di dim zeri.
# •	Per ogni parola del testo (minuscola) si calcola un numero con md5, e numero % dim dà una posizione del vettore tra 0 e dim - 1: lì si somma 1. 
# Parole uguali finiscono nella stessa posizione. È un trucco semplice per ottenere un vettore di lunghezza fissa.
# •	Se normalizza è vero, il vettore viene diviso per la sua lunghezza n, così da avere lunghezza 1.
# 3. La classe ModelliFinti, metodo embed_content imita la chiamata di Gemini.
# •	Controlla che il modello sia uno dei due noti, altrimenti solleva un errore.
# •	La dimensione viene letta dalla configurazione (output_dimensionality) e vale 3072 se non c’è.
# •	Se contents è una stringa la mette in una lista di un elemento.
# •	Con gemini-embedding-2 e più testi riunisce tutto in un solo testo: imita l’embedding aggregato.
# •	Con gemini-embedding-001 e una dimensione diversa da 3072 restituisce vettori non normalizzati, come descritto nella documentazione.
# •	Restituisce un oggetto con embeddings, una lista in cui ogni elemento ha un attributo values (il vettore).
# 4. client e types. client = SimpleNamespace(models=ModelliFinti()) crea un oggetto con client.models.embed_content, e types.EmbedContentConfig(...) costruisce la configurazione, 
# come in google.genai.
# 5. DOCUMENTI è un piccolo archivio di 4 testi (resi, rimborsi, spedizioni, pagamenti) con id, titolo e testo. Lo usano gli esercizi dal 15 al 20.


import hashlib, math, re
from types import SimpleNamespace

def _vettore(testo, dim, normalizza=True):
    testo = re.sub(r"^(?:task|title):[^|]*\|\s*(?:query|text):\s*", "", testo)
    v = [0.0] * dim
    for parola in re.findall(r"\w+", testo.lower()):
        numero = int(hashlib.md5(parola.encode("utf-8")).hexdigest(), 16)
        v[numero % dim] += 1.0
    n = math.sqrt(sum(x * x for x in v))
    if normalizza and n > 0:
        v = [x / n for x in v]
    return v

class ModelliFinti:
    def embed_content(self, model, contents, config=None):
        if model not in ("gemini-embedding-001", "gemini-embedding-2"):
            raise ValueError(f"modello sconosciuto: {model}")
        dim = getattr(config, "output_dimensionality", None) or 3072
        testi = [contents] if isinstance(contents, str) else list(contents)
        if model == "gemini-embedding-2" and len(testi) > 1:
            testi = [" ".join(testi)]
        normalizza = not (model == "gemini-embedding-001" and dim != 3072)
        vettori = [_vettore(t, dim, normalizza) for t in testi]
        return SimpleNamespace(embeddings=[SimpleNamespace(values=v) for v in vettori])

client = SimpleNamespace(models=ModelliFinti())
types = SimpleNamespace(EmbedContentConfig=lambda **kw: SimpleNamespace(**kw))

DOCUMENTI = [
    {"id": 0, "titolo": "Resi", "testo": "Il reso è gratuito entro quattordici giorni dalla consegna."},
    {"id": 1, "titolo": "Rimborsi", "testo": "Il rimborso arriva entro sette giorni dal ricevimento del reso."},
    {"id": 2, "titolo": "Spedizioni", "testo": "La spedizione costa cinque euro e la consegna avviene in tre giorni."},
    {"id": 3, "titolo": "Pagamenti", "testo": "Si accettano carta di credito e bonifico bancario."},
]
