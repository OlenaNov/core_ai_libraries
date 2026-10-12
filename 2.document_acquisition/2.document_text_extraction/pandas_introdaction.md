**Pandas** è una delle librerie più popolari e potenti di **Python**, utilizzata principalmente per la **manipolazione e l'analisi dei dati** (*Data Analysis* e *Data Science*). 

Il suo nome deriva dal termine econometrico *"Panel Data"* (dati panel), che indica set di dati multidimensionali, ma è anche un gioco di parole con "Python Data Analysis".

Ecco una panoramica delle sue caratteristiche principali:

---

### 1. A cosa serve?
Pandas viene usato per:
* **Importare ed esportare dati** da diversi formati (CSV, Excel, JSON, database SQL, HTML, ecc.).
* **Pulire i dati** (gestire valori mancanti, correggere formati di testo o date).
* **Filtrare, ordinare e raggruppare** grandi quantità di dati in modo efficiente.
* **Analisi statistica di base** (medie, mediane, correlazioni).
* **Preparare i dati** per essere utilizzati in modelli di Machine Learning (spesso in combinazione con librerie come Scikit-Learn).

---

### 2. Le strutture dati principali
Pandas si basa su due strutture dati fondamentali, entrambe costruite sopra la libreria **NumPy**:

1. **`Series`**: È un array unidimensionale etichettato (simile a una colonna di una tabella o a un dizionario).
2. **`DataFrame`**: È la struttura principale di Pandas. È una tabella bidimensionale con righe e colonne etichettate (molto simile a un foglio di calcolo di Excel o a una tabella SQL).

---

### 3. Un esempio pratico

Ecco come appare del codice Pandas per creare e manipolare un piccolo DataFrame:

```python
import pandas as pd

# Creazione di un DataFrame da un dizionario
dati = {
    'Nome': ['Anna', 'Luca', 'Marco', 'Giulia'],
    'Età': [25, 30, 35, 28],
    'Città': ['Roma', 'Milano', 'Napoli', 'Torino']
}

df = pd.DataFrame(dati)

# Visualizza la tabella
print(df)

# Filtra le persone con età superiore a 28 anni
esperti = df[df['Età'] > 28]
print(esperti)
```

---

### 4. Perché è così popolare?
* **Integrazione:** Lavora benissimo con altre librerie dell'ecosistema Python come NumPy, Matplotlib (per la visualizzazione dei dati) e Scikit-Learn.
* **Velocità:** Molte operazioni sono scritte in C sotto il capot, rendendole molto veloci anche con dataset di milioni di righe.
* **Sintassi intuitiva:** È relativamente facile da imparare rispetto ad altri strumenti di analisi dati.