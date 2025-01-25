from collections import defaultdict

import pandas as pd

import string
import asyncio
import deepl
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from googletrans import Translator
import nltk
from sklearn.model_selection import train_test_split

#risorse nltk
nltk.download('punkt')
nltk.download('stopwords')

dataset = pd.read_csv("../dataset_finale_bilanciato.csv", sep='\t', header=None)

dataset = dataset.drop(index=0)




# Separiamo la colonna in due per testo ed emozione
dataset[['0', '1']] = dataset[0].str.split(',', expand=True, n=1)


dataset['1'] = dataset['1'].astype(str)

# Rimuoviamo la colonna originale che ora è separata
df_filtered = dataset.drop(columns=[0])


# Funzione per preprocessare il testo e normalizzarlo
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    # Convertiamo in minuscolo
    text = text.lower()
    # Rimuoviamo la punteggiatura
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Tokenizziamo il testo
    words = word_tokenize(text)
    # Rimuoviamo le stopwords
    words = [word for word in words if word not in stop_words]
    return " ".join(words)


df_filtered['0']=df_filtered['0'].apply(preprocess_text)

# Suddivisione in training set e test set
train_set, test_set = train_test_split(df_filtered, test_size=0.2, random_state=42)




# Calcolo delle frequenze nel training set
emozione_counts = train_set['1'].value_counts().to_dict()
totale_messaggi = len(train_set)

# Calcolo della frequenza delle parole per emozione
parole_per_emozione = defaultdict(list)
for idx, row in train_set.iterrows():
    parole = row['0'].split()  # Ottieni le parole preprocessate
    parole_per_emozione[row['1']].extend(parole)

# Calcolo della frequenza totale delle parole nel training set
frequenza_totale_parole = defaultdict(int)
for testo_normalizzato in train_set['0']:
    for parola in testo_normalizzato.split():
        frequenza_totale_parole[parola] += 1

# Funzioni per calcolare le probabilità
def calcola_prob_emozione(emozione):
    return emozione_counts.get(emozione, 0) / totale_messaggi

def calcola_prob_parola_emozione(parola, emozione):
    parole = parole_per_emozione[emozione]
    totale_parole = len(parole)
    frequenza_parola = parole.count(parola)
    return (frequenza_parola + 1) / (totale_parole + len(frequenza_totale_parole))

def calcola_prob_parola(parola):
    """P(parola): frequenza della parola nel dataset"""
    totale_parole_dataset = sum(frequenza_totale_parole.values())
    frequenza_parola = frequenza_totale_parole.get(parola, 0)
    return frequenza_parola / totale_parole_dataset


def calcola_prob_emozione_messaggio(messaggio, emozione):
    parole = messaggio.split()  # Il messaggio è già preprocessato
    prob_parola_emozione = 1

    # Moltiplichiamo la probabilità di ciascuna parola condizionata dall'emozione
    for parola in parole:
        prob_parola_emozione *= calcola_prob_parola_emozione(parola, emozione)

    # Calcoliamo la probabilità della singola parola P(w_i) nel dataset
    prob_parola_indipendente = 1
    for parola in parole:
        prob_parola_indipendente *= calcola_prob_parola(parola)

    # Probabilità a priori dell'emozione
    prob_emozione = calcola_prob_emozione(emozione)

    # Calcoliamo la probabilità finale con il Teorema di Bayes, considerando la parola indipendente
    prob_emozione_messaggio = prob_emozione * prob_parola_emozione * prob_parola_indipendente

    return prob_emozione_messaggio

def predici_emozione(messaggio):
    probabilita_emozioni = {
        emozione: calcola_prob_emozione_messaggio(messaggio, emozione)
        for emozione in emozione_counts.keys()
    }
    return max(probabilita_emozioni, key=probabilita_emozioni.get)

# Funzione per caricare messaggi da un file di testo
def carica_test_da_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    messaggi = [line.strip().split('\t') for line in lines if line.strip()]
    # Assumiamo che il file contenga: testo \t emozione_reale
    return [(preprocess_text(m[0]), m[1]) for m in messaggi]

# Caricamento del file di test
test_file_path = "test_messages.txt"  # Inserisci il percorso al tuo file di test
test_messaggi = carica_test_da_file(test_file_path)

# Calcolo delle predizioni e dell'accuratezza
errori = []
totale_test = len(test_messaggi)
corretti = 0

for messaggio, emozione_reale in test_messaggi:
    predizione = predici_emozione(messaggio)
    if predizione == emozione_reale:
        corretti += 1
    else:
        errori.append({
            "messaggio": messaggio,
            "emozione_reale": emozione_reale,
            "emozione_predetta": predizione
        })

# Risultati
accuracy = corretti / totale_test
print(f"Accuratezza finale: {accuracy:.4f}")

# Messaggi con predizioni errate
print("\nMESSAGGI CON PREDIZIONI ERRATE:")
for errore in errori:
    print(f"Messaggio: {errore['messaggio']}")
    print(f"Emozione reale: {errore['emozione_reale']}")
    print(f"Emozione predetta: {errore['emozione_predetta']}")
    print("-" * 50)







