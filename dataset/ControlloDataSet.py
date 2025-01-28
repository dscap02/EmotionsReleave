import pandas as pd

# Caricare il dataset pulito
file_path = '../dataset_filtrato_pulito.csv'  # Sostituisci con il percorso corretto
df = pd.read_csv(file_path)

# Assumendo che la colonna delle emozioni sia la seconda colonna (indice 1)
df['emozioni'] = df[df.columns[1]].astype(str).str.split(',')

# Trova le righe con più di un'emozione assegnata
multi_emotion_instances = df[df['emozioni'].apply(len) > 1]

# Se ci sono istanze con emozioni correlate, stamparle
if not multi_emotion_instances.empty:
    print("Istanze con emozioni correlate trovate:")
    for index, row in multi_emotion_instances.iterrows():
        message = row[df.columns[0]]  # Messaggio
        emotions = ', '.join(row['emozioni'])
        print(f"Messaggio: {message} - Emozioni: {emotions}")
else:
    print("Nessuna istanza con emozioni multiple trovata.")