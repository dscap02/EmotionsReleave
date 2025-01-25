import pandas as pd
from collections import Counter

# Carica il dataset
dataset = pd.read_csv("train.tsv", sep='\t', header=None)

# Mappa delle emozioni
emotion_map = {
    0: "Ammirazione",
    1: "Divertimento",
    2: "Rabbia",
    3: "Fastidio",
    4: "Approvazione",
    5: "Premura",
    6: "Confusione",
    7: "Curiosità",
    8: "Desiderio",
    9: "Delusione",
    10: "Disapprovazione",
    11: "Disgusto",
    12: "Imbarazzo",
    13: "Entusiasmo",
    14: "Paura",
    15: "Gratitudine",
    16: "Dolore",
    17: "Gioia",
    18: "Amore",
    19: "Nervosismo",
    20: "Ottimismo",
    21: "Orgoglio",
    22: "Consapevolezza",
    23: "Sollievo",
    24: "Rimorso",
    25: "Tristezza",
    26: "Sorpresa",
    27: "Neutra"
}

# Separare le emozioni multiple
dataset[1] = dataset[1].str.split(',')

# Inizializza un dizionario per conteggiare le correlazioni
correlations = {emotion: Counter() for emotion in range(28)}  # 28 emozioni (da 0 a 27)
emotion_instances = {emotion: 0 for emotion in range(28)}  # Conteggio delle istanze per ogni emozione

# Calcola le correlazioni e le istanze per ogni emozione
for emotions in dataset[1]:
    for emotion in emotions:
        emotion = int(emotion)
        emotion_instances[emotion] += 1  # Conta le istanze
        # Aggiungi tutte le altre emozioni presenti nella stessa riga
        for co_emotion in emotions:
            co_emotion = int(co_emotion)
            if emotion != co_emotion:  # Evita l'autocorrelazione
                correlations[emotion][co_emotion] += 1

# Output: Frequenze totali, correlazioni e istanze per ogni emozione
for emotion, co_emotions in correlations.items():
    print(f"Emozione {emotion_map[emotion]} ({emotion}):")
    print(f"  Istanze totali: {emotion_instances[emotion]}")
    print(f"  Frequenza totale (collegamenti): {sum(co_emotions.values())}")

    # Ordinamento delle emozioni correlate in ordine crescente
    sorted_correlations = sorted(co_emotions.items(), key=lambda x: x[1])

    for co_emotion, count in sorted_correlations:
        print(f"    Si collega con emozione {emotion_map[co_emotion]} ({co_emotion}) {count} volte")
    print("\n")
