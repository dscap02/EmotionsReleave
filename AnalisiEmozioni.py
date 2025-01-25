import pandas as pd

# Funzione per determinare se una riga contiene la coppia di emozioni 0 e 24
def contains_emotions_0_14(emotions):
    # Converte la stringa delle emozioni in una lista di interi
    emotion_list = list(map(int, emotions.split(',')))
    # Controlla se entrambe le emozioni 0 e 24 sono presenti
    return 0 in emotion_list and 5 in emotion_list

# Leggi il dataset
dataset = pd.read_csv("train.tsv", sep='\t', header=None)

# Filtra le righe che contengono la coppia di emozioni (0, 24)
df_with_0_14 = dataset[dataset[1].apply(contains_emotions_0_14)]



# Scrivere l'output in un file di testo
with open("output.txt", "w",encoding='utf-8') as file:
    file.write(df_with_0_14.to_string(index=False))

# Stampa un messaggio per confermare che il file è stato creato
print("Istanze con le emozioni 0 e 24 sono state scritte nel file 'output.txt'")
