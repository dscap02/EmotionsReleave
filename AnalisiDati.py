import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import table
import unicodedata

# Funzione per rimuovere caratteri speciali
def remove_special_chars(text):
    return ''.join(c for c in text if unicodedata.category(c) != 'So')  # Rimuove emoticon e simboli

# Caricare il file TSV
dataset = pd.read_csv("train.tsv", sep='\t', header=None)

# Filtrare i messaggi che contengono '0' nella colonna 1
filtered_dataset = dataset[dataset[1].apply(lambda x: '0' in str(x).split(','))]

# Rinomina le colonne per una visualizzazione più chiara
filtered_dataset.columns = ['Message', 'Emotions', 'ID']

# Rimuovi eventuali caratteri speciali dai messaggi
filtered_dataset['Message'] = filtered_dataset['Message'].apply(remove_special_chars)

# Crea una figura per la tabella con dimensioni adeguate
fig, ax = plt.subplots(figsize=(12, 6))  # Puoi cambiare queste dimensioni in base alle necessità
ax.axis('off')  # Nascondi gli assi

# Aggiungi la tabella con un font più piccolo per evitare che il testo esca dai bordi
tbl = table(ax, filtered_dataset, loc='center', colWidths=[0.3, 0.3, 0.2])

# Ridimensiona il testo per adattarlo meglio alle celle
tbl.auto_set_font_size(False)
tbl.set_fontsize(8)

# Salva la tabella in un file PDF
plt.savefig("filtered_dataset.pdf", bbox_inches='tight')  # Salva in PDF

# Conferma
print("Tabella salvata come 'filtered_dataset.pdf'")
