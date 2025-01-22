import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import table
from matplotlib import rcParams
import unicodedata

# Imposta un font che supporti caratteri speciali (come emoji e ideogrammi CJK)
rcParams['font.family'] = 'DejaVu Sans'  # Puoi sostituire con 'Noto Sans' se installato

# Funzione per rimuovere caratteri speciali indesiderati
def remove_special_chars(text):
    return ''.join(c for c in text if unicodedata.category(c) != 'So')  # Rimuove emoticon e simboli non necessari

# Carica il file TSV
dataset = pd.read_csv("train.tsv", sep='\t', header=None)

# Filtra i messaggi che contengono '0' nella colonna 1
filtered_dataset = dataset[dataset[1].apply(lambda x: '0' in str(x).split(','))]

# Rinomina le colonne per una visualizzazione più chiara
filtered_dataset.columns = ['Message', 'Emotions', 'ID']

# Rimuovi eventuali caratteri speciali indesiderati dai messaggi
filtered_dataset['Message'] = filtered_dataset['Message'].apply(remove_special_chars)

# Elimina la colonna degli ID
filtered_dataset = filtered_dataset[['Message', 'Emotions']]

# Crea una figura per la tabella con dimensioni adeguate
fig, ax = plt.subplots(figsize=(14, 8))  # Dimensioni maggiori per migliore leggibilità
ax.axis('off')  # Nascondi gli assi

# Crea la tabella
tbl = table(ax, filtered_dataset, loc='center', colWidths=[0.7, 0.3])  # Adatta le larghezze delle colonne

# Configura il testo della tabella
tbl.auto_set_font_size(False)
tbl.set_fontsize(8)

# Adatta l'altezza delle righe e abilita il wrapping del testo
for key, cell in tbl.get_celld().items():
    cell.set_text_props(wrap=True)
    cell.set_height(0.05)  # Aumenta l'altezza delle righe per migliorare il layout

# Salva la tabella in un file PDF
plt.savefig("formatted_filtered_dataset_no_id.pdf", bbox_inches='tight')  # Salva in PDF

# Conferma
print("Tabella salvata come 'formatted_filtered_dataset_no_id.pdf'")
