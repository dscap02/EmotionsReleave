import pandas as pd

# Funzione per sostituire le combinazioni 0,14 con 14
def replace_emotions_conditionally(emotions, values_to_replace, replacement_value):
    # Converte la stringa delle emozioni in una lista di interi
    emotion_list = list(map(int, emotions.split(',')))
    # Controlla se ci sono emozioni da sostituire
    if any(e in values_to_replace for e in emotion_list):
        return str(replacement_value)  # Trasforma tutto in 14
    return emotions  # Mantiene il messaggio originale

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
#Eliminiamo le correlazioni 0 e 19
df_filtered = df_filtered[~df_filtered[1].apply(lambda x: contains_correlations(x, correlation_to_remove))]

#Eliminaimo le corelazioni {0,16}
correlation_to_remove = {0, 16}
df_filtered = df_filtered[~df_filtered[1].apply(lambda x: contains_correlations(x, correlation_to_remove))]

#Eliminaimo le correlazioni {0,12}
correlation_to_remove = {0, 12}
df_filtered = df_filtered[~df_filtered[1].apply(lambda x: contains_correlations(x, correlation_to_remove))]


#Accorpamento emozioni {0,14} in {14}
values_to_replace = [0, 14]
replacement_value = 14
df_filtered[1] = df_filtered[1].apply(
    lambda x: replace_emotions_conditionally(x, values_to_replace, replacement_value)
)

#Eliminioamo le correlazioni {0,23}
correlation_to_remove = {0, 23}
df_filtered = df_filtered[~df_filtered[1].apply(lambda x: contains_correlations(x, correlation_to_remove))]

#Eliminioamo le correlazioni {0,2}
correlation_to_remove = {0, 2}
df_filtered = df_filtered[~df_filtered[1].apply(lambda x: contains_correlations(x, correlation_to_remove))]

#Eliminioamo le correlazioni {0,24}
correlation_to_remove = {0, 24}
df_filtered = df_filtered[~df_filtered[1].apply(lambda x: contains_correlations(x, correlation_to_remove))]

#Eliminioamo le correlazioni {0,11}
correlation_to_remove = {0, 11}
df_filtered = df_filtered[~df_filtered[1].apply(lambda x: contains_correlations(x, correlation_to_remove))]

#Eliminioamo le correlazioni {0,10}
correlation_to_remove = {0, 10}
df_filtered = df_filtered[~df_filtered[1].apply(lambda x: contains_correlations(x, correlation_to_remove))]

#Eliminioamo le correlazioni {0,25} perchè sono troppo incasinate
correlation_to_remove = {0, 25}
df_filtered = df_filtered[~df_filtered[1].apply(lambda x: contains_correlations(x, correlation_to_remove))]

#Accorpamento emozioni {0,21} in {0}
values_to_replace = [0, 21]
replacement_value = 0
df_filtered[1] = df_filtered[1].apply(
    lambda x: replace_emotions_conditionally(x, values_to_replace, replacement_value)
)

#Eliminioamo le correlazioni {0,6} perchè sono troppo incasinate
correlation_to_remove = {0, 6}
df_filtered = df_filtered[~df_filtered[1].apply(lambda x: contains_correlations(x, correlation_to_remove))]

#Eliminioamo le correlazioni {0,9} perchè sono troppo incasinate
correlation_to_remove = {0, 9}
df_filtered = df_filtered[~df_filtered[1].apply(lambda x: contains_correlations(x, correlation_to_remove))]

#Eliminioamo le correlazioni {0,3} perchè sono troppo incasinate
correlation_to_remove = {0, 3}
df_filtered = df_filtered[~df_filtered[1].apply(lambda x: contains_correlations(x, correlation_to_remove))]

#Accorpamento emozioni {0,5} in {0}
values_to_replace = [0, 5]
replacement_value = 0
df_filtered[1] = df_filtered[1].apply(
    lambda x: replace_emotions_conditionally(x, values_to_replace, replacement_value)
)

#Accorpamento emozioni {0,8} in {0}
values_to_replace = [0, 8]
replacement_value = 0
df_filtered[1] = df_filtered[1].apply(
    lambda x: replace_emotions_conditionally(x, values_to_replace, replacement_value)
)

#Eliminioamo le correlazioni {0,22} perchè sono troppo incasinate
correlation_to_remove = {0, 22}
df_filtered = df_filtered[~df_filtered[1].apply(lambda x: contains_correlations(x, correlation_to_remove))]

#Eliminioamo le correlazioni {0,26} perchè sono troppo incasinate
correlation_to_remove = {0, 26}
df_filtered = df_filtered[~df_filtered[1].apply(lambda x: contains_correlations(x, correlation_to_remove))]

#Eliminioamo le correlazioni {0,7} perchè sono troppo incasinate
correlation_to_remove = {0, 7}
df_filtered = df_filtered[~df_filtered[1].apply(lambda x: contains_correlations(x, correlation_to_remove))]

#Accorpamento emozioni {0,13} in {13}
values_to_replace = [0, 13]
replacement_value = 13
df_filtered[1] = df_filtered[1].apply(
    lambda x: replace_emotions_conditionally(x, values_to_replace, replacement_value)
)

#Accorpamento emozioni {0,1} in {1}
values_to_replace = [0, 1]
replacement_value = 1
df_filtered[1] = df_filtered[1].apply(
    lambda x: replace_emotions_conditionally(x, values_to_replace, replacement_value)
)

#Accorpamento emozioni {0,20} in {0}
values_to_replace = [0, 20]
replacement_value = 0
df_filtered[1] = df_filtered[1].apply(
    lambda x: replace_emotions_conditionally(x, values_to_replace, replacement_value)
)

#Accorpamento emozioni {0,17} in {17}
values_to_replace = [0, 17]
replacement_value = 17
df_filtered[1] = df_filtered[1].apply(
    lambda x: replace_emotions_conditionally(x, values_to_replace, replacement_value)
)

#Accorpamento emozioni {0,18} in {18}
values_to_replace = [0, 18]
replacement_value = 18
df_filtered[1] = df_filtered[1].apply(
    lambda x: replace_emotions_conditionally(x, values_to_replace, replacement_value)
)

#Accorpamento emozioni {0,4} in {0}
values_to_replace = [0, 4]
replacement_value = 0
df_filtered[1] = df_filtered[1].apply(
    lambda x: replace_emotions_conditionally(x, values_to_replace, replacement_value)
)

#Accorpamento emozioni {0,15} in {0}
values_to_replace = [0, 15]
replacement_value = 0
df_filtered[1] = df_filtered[1].apply(
    lambda x: replace_emotions_conditionally(x, values_to_replace, replacement_value)
)

df_filtered.to_csv("dataset_filtrato.csv", index=False)

print("File salvato come 'dataset_filtrato.csv'")
