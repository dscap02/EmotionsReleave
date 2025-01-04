import pandas as pd

# Funzione per sostituire le combinazioni 0,14 con 14
def replace_emotions(emotions):
    # Converte la stringa delle emozioni in una lista di interi
    emotion_list = list(map(int, emotions.split(',')))
    # Se 0 e 14 sono presenti, li sostituiamo entrambi con 14
    if 0 in emotion_list and 14 in emotion_list:
        emotion_list = [14 if (e == 0 or e == 14) else e for e in emotion_list]
    # Ritorna la lista modificata come stringa
    return ','.join(map(str, sorted(emotion_list)))

# Funzione per determinare se una riga deve essere eliminata in base a una correlazione generica
def contains_correlations(emotions, correlation_set):
    # Converte la stringa di emozioni in un set di interi
    emotion_set = set(map(int, emotions.split(',')))
    # Verifica se il set di correlazioni da eliminare è un sottoinsieme delle emozioni nella riga
    return correlation_set.issubset(emotion_set)

# Funzione per determinare se una riga deve essere eliminata (condizione originale)
def should_remove(emotions):
    # Converte la stringa di emozioni in una lista di interi
    emotion_list = list(map(int, emotions.split(',')))
    # Controlla se contiene 27 e almeno un'altra emozione
    return 27 in emotion_list and len(emotion_list) > 1

# Leggi il dataset
dataset = pd.read_csv("train.tsv", sep='\t', header=None)

# Applica il filtro per rimuovere le righe che soddisfano la condizione originale
df_filtered = dataset[~dataset[1].apply(should_remove)]

# Definisci la correlazione da eliminare
correlation_to_remove = {0, 19}



# Applica il filtro per rimuovere le righe in base alla correlazione generica
#Eliminiamo le emozioni 0 e 19
df_filtered = df_filtered[~df_filtered[1].apply(lambda x: contains_correlations(x, correlation_to_remove))]

#Eliminaimo le emozioni {0,16}
correlation_to_remove = {0, 16}
df_filtered = df_filtered[~df_filtered[1].apply(lambda x: contains_correlations(x, correlation_to_remove))]

#Eliminaimo le emozioni {0,12}
correlation_to_remove = {0, 12}
df_filtered = df_filtered[~df_filtered[1].apply(lambda x: contains_correlations(x, correlation_to_remove))]


#Accorpamento emozioni {0,14} in {14}
df_filtered[1]=df_filtered[1].apply(replace_emotions)





# Conta i valori nulli nella colonna 0
#null_count_col_0 = dataset.iloc[:, 0].isnull().sum()

# Conta i valori nulli nella colonna 1
#null_count_col_1 = dataset.iloc[:, 1].isnull().sum()

# Stampa i risultati
#print(f"Valori nulli nella colonna 0: {null_count_col_0}")
#print(f"Valori nulli nella colonna 1: {null_count_col_1}")
