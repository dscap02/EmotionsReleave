# utils.py
from turtle import st

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F
from datetime import datetime

# Caricamento del modello pre-addestrato GoEmotions
MODEL_NAME = "bhadresh-savani/bert-base-uncased-emotion"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

# Dizionario delle emozioni (dal modello GoEmotions)
EMOTIONS = [
    "admiration", "amusement", "anger", "annoyance", "approval", "caring", "confusion", "curiosity",
    "desire", "disappointment", "disapproval", "disgust", "embarrassment", "excitement", "fear", "gratitude",
    "grief", "joy", "love", "nervousness", "optimism", "pride", "realization", "relief", "remorse",
    "sadness", "surprise", "neutral"
]


# Funzione per classificare l'emozione
def classify_emotion(text):
    # Tokenizzazione del testo
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)

    # Predizione
    outputs = model(**inputs)
    probabilities = F.softmax(outputs.logits, dim=1)

    # Seleziona l'emozione più probabile
    max_index = torch.argmax(probabilities, dim=1).item()
    emotion = EMOTIONS[max_index]
    confidence = probabilities[0, max_index].item()

    return emotion, confidence


# Funzione per caricare una chat da un file di testo
def load_chat_from_file(uploaded_file):
    chat = []
    try:
        # Leggi il contenuto del file
        content = uploaded_file.getvalue().decode("utf-8")

        # Dividi il contenuto in righe
        lines = content.splitlines()

        # Analizza ogni riga per separare interlocutore e messaggio
        for line in lines:
            # Ignora righe vuote
            if line.strip():
                # Assumiamo che il formato sia "Interlocutore X: Messaggio"
                if ": " in line:
                    interlocutor, text = line.split(": ", 1)
                    chat.append({"interlocutor": interlocutor.strip(), "text": text.strip()})

        if not chat:
            st.error("Nessun messaggio rilevato nel file.")
        return chat

    except Exception as e:
        st.error(f"Errore nel caricare il file: {e}")
        return []


# Funzione per generare un report della conversazione
def generate_report(conversation):
    report = f"Report Generato il {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

    # Aggiungi per ogni messaggio dell'interlocutore l'emozione e la confidenza
    for speaker, message in conversation:
        emotion, confidence = classify_emotion(message)
        report += f"**{speaker}:** {message}\n"
        report += f"  Emozione: {emotion} (Confidenza: {confidence:.2f})\n\n"

    return report
