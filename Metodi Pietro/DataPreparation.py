from collections import Counter
from textblob import download_corpora


import pandas as pd


from textblob import TextBlob
from textblob import download_corpora
download_corpora.download_all()


# Funzione per sostituire le combinazioni 0,14 con 14
def replace_emotions(emotions):
    # Converte la stringa delle emozioni in una lista di interi
    emotion_list = list(map(int, emotions.split(',')))
    # Se 0 e 14 sono presenti, li sostituiamo entrambi con 14
    if 0 in emotion_list and 14 in emotion_list:
        emotion_list = [14 if (e == 0 or e == 14) else e for e in emotion_list]
    # Ritorna la lista modificata come stringa
    return ','.join(map(str, sorted(emotion_list)))


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

#Funzione per controllare se le emozioni correlate sono presenti nel dataset filtrato
def contains_emotions(emotions):
    # Converte la stringa delle emozioni in una lista di interi
    emotion_list = list(map(int, emotions.split(',')))
    # Controlla se entrambe le emozioni 0 e 24 sono presenti
    return 1 in emotion_list

#Funzione per determinare le istanze con una singola emozione
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



#Eliminazione istanze emozioni correlate(Divertimento,orgoglio),perchè correlazione rara

correlation_to_remove={1,21}
df_filtered=df_filtered[~df_filtered[1].apply(lambda x: contains_correlations(x, correlation_to_remove))]

#dataframe per controllo presenza istanze con emozioni correlate specificate
df_with = df_filtered[df_filtered[1].apply(contains_emotions)]

#print(df_with)


#Eliminazione istanze emozioni correlate(Divertimento,Nervosismo),perchè correlazione rara

correlation_to_remove={1,19}
df_filtered=df_filtered[~df_filtered[1].apply(lambda x: contains_correlations(x, correlation_to_remove))]
df_with=df_filtered[df_filtered[1].apply(contains_emotions)]

#print(df_with)

#Eliminazione istanze emozioni correlate(Divertimento,Paura),con presenza correlazione rara
correlation_to_remove={1,14}
df_filtered=df_filtered[~df_filtered[1].apply(lambda x: contains_correlations(x, correlation_to_remove))]
df_with=df_filtered[df_filtered[1].apply(contains_emotions)]
#print(df_with)

#Eliminazione istanze emozioni correlate(Divertimento,Sollievo),con presenza correlazione rara
correlation_to_remove={1,23}
df_filtered=df_filtered[~df_filtered[1].apply(lambda x: contains_correlations(x, correlation_to_remove))]
df_with=df_filtered[df_filtered[1].apply(contains_emotions)]
#print(df_with)


#Vocabolario che tiene conto di tutte le parole estratte dai messaggi con relativi indici
vocabulary = {"lol":0,"Lol":1,"funny":2,"haha":3,"fun":4,"Haha":5,"joke":6,"hilarious":7,"LOL":8,"laugh":9,"lmao":10,"Lmao":11,"Funny":12,"LMAO":13,"entertaining":14,"chuckle":15,"Fun":16,"JOKE":17,
"Hilarious":18,"LMao":19,"rofl":20,"Chuckle":21,"HaHa":22,"amusing":23,"laughter":24,"Rofl":25,"Amusing":26,"FUN":27,"Joke":28,"Laugh":29,"ROFL":30}


target_emotion=1
#Filtro istanze contenenti solo l'emozione principale(Divertimento)
df_divertimento=df_filtered[df_filtered[1].apply(lambda emotions: has_specific_single_emotion(emotions, target_emotion))]
#print(df_divertimento)

#Estrazione parole chiavi da istanze con emozione(Divertimento),per aggiungere e formare un set più completo
#Estrazione delle parole da tutti i messaggi
vocab_frequency = {word: 0 for word in vocabulary}
for text in df_divertimento[0]:
    #controlliamo che siano stringhe
    if not isinstance(text, str):
        text = str(text)

    blob = TextBlob(text.lower())
    #Estrazione parole e conteggio frequenza
    for word in blob.words:
         if word in vocabulary:
             vocab_frequency[word]+=1


# Parole chiave più frequenti
sorted_vocab_frequency = sorted(vocab_frequency.items(), key=lambda x: x[1], reverse=True)

#Salvo tutte le parole chiavi con frequenza più alta
KeywordsFrequency={}
for word, freq in sorted_vocab_frequency:
    if freq > 5:
        KeywordsFrequency[word]=freq

Keywords={"premura": ["care", "worry", "support", "help", "keep going"]}
#print(KeywordsFrequency)


#filtriamo il dataset per ottenere esclusivamente le istanza con correlazione(divertimento,premura)
def contains_emotions(emotions):
    # Converte la stringa delle emozioni in una lista di interi
    emotion_list = list(map(int, emotions.split(',')))
    # Controlla se entrambe le emozioni 1 e 5 sono presenti
    return 1 in emotion_list and 5 in emotion_list

df_with=df_filtered[df_filtered[1].apply(contains_emotions)]

#print(df_with)

#Individuazione emozione predominante in base al conteggio delle parole chiavi relative a (divertimento,premura) e al tono e attitudine della frase

def classify_emotions_with_sentiment(text):
    blob = TextBlob(text.lower())
    words_premura = Keywords
    words_divertimento=KeywordsFrequency

    words = blob.words

    count_divertimento = sum(1 for word in words if word in words_divertimento)
    count_premura = sum(1 for word in words if word in words_premura)

    #analizzando il tono della frase
    sentiment = blob.sentiment.polarity

    if count_premura > count_divertimento:
        return "premura"
    elif count_divertimento > count_premura:
        return "divertimento"
    else:
        if sentiment > 0:
            return "divertimento"  # Sentiment positivo suggerisce divertimento
        elif sentiment < 0:
            return "premura"


risultato= df_with[0].apply(
    lambda text: classify_emotions_with_sentiment(text)
)

# Visualizza il DataFrame con l'emozione predominante
print(risultato)













