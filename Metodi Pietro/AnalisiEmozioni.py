import pandas as pd

from DataPreparation import target_emotion, df_filtered


# Funzione per determinare se una riga contiene la coppia di emozioni 0 e 24
def contains_emotions(emotions):
    # Converte la stringa delle emozioni in una lista di interi
    emotion_list = list(map(int, emotions.split(',')))
    # Controlla se entrambe le emozioni 0 e 24 sono presenti
    return 1 in emotion_list and 5 in emotion_list

#Funzione per ottenre le istanze con singola emozione in output
def has_specific_single_emotion(emotions, target_emotion):
    """
    Controlla se una stringa di emozioni contiene solo una specifica emozione.

    :param emotions: Una stringa contenente emozioni separate da virgola (es. "1,24,5").
    :param target_emotion: L'emozione specifica da cercare (int).
    :return: True se c'è solo l'emozione specificata, False altrimenti.
    """
    # Converte la stringa delle emozioni in una lista di interi
    emotion_list = list(map(int, emotions.split(',')))
    # Controlla se la lista contiene solo l'emozione specificata
    return len(emotion_list) == 1 and emotion_list[0] == target_emotion

# Leggi il dataset
dataset = pd.read_csv("../train.tsv", sep='\t', header=None)

# Filtra le righe che producono come output un'unica emozione(divertimento)
target_emotion=1
#df_with= df_filtered[df_filtered[1].apply(lambda emotions: has_specific_single_emotion(emotions, target_emotion))]

df_with=df_filtered[df_filtered[1].apply(contains_emotions)]


# Scrivere l'output in un file di testo
with open("../output.txt", "w", encoding="utf-8") as file:
    file.write("Istanze con l'emozione 1:\n")
    file.write(df_with.to_string(index=False))

# Stampa un messaggio per confermare che il file è stato creato
print("Istanze con l'emozione sono state scritte nel file 'output.txt'")
