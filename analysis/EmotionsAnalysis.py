import pandas as pd

def filter_rows_with_emotions(dataset, x, y):
    """
    Filtra le righe di un dataset in cui la colonna delle emozioni contiene entrambe le emozioni x e y.

    :param dataset: DataFrame contenente il dataset
    :param x: Indice della prima emozione
    :param y: Indice della seconda emozione
    :return: DataFrame filtrato
    """
    def contains_emotions(emotions):
        # Converte la stringa delle emozioni in una lista di interi
        emotion_list = list(map(int, emotions.split(',')))
        # Controlla se entrambe le emozioni x e y sono presenti
        return x in emotion_list and y in emotion_list

    # Applica il filtro al dataset
    return dataset[dataset[1].apply(contains_emotions)]

# Assegna l'indice dell'emozione x
emotion_x = 10

# Leggi il dataset
dataset = pd.read_csv("train.tsv", sep='\t', header=None)

# Scrivere l'output in un file di testo
with open("output.txt", "w", encoding="utf-8") as file:
    for emotion_y in range(27):
        if emotion_x != emotion_y:
            # Filtra le righe che contengono le emozioni specificate
            df_with_emotions = filter_rows_with_emotions(dataset, emotion_x, emotion_y)
            if not df_with_emotions.empty:  # Controlla se il DataFrame non è vuoto
                file.write(f"Istanze con le emozioni {emotion_x} e {emotion_y}:\n")
                file.write(df_with_emotions.to_string(index=False))
                file.write("\n\n")


# Stampa un messaggio per confermare che il file è stato creato
print(f"Tutte le istanze con l'emozione {emotion_x} e ogni altra emozione da 0 a 26 sono state scritte nel file 'output.txt'")
