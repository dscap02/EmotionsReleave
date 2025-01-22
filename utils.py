# utils.py


import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F
from datetime import timedelta

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
from datetime import datetime




def load_chat_from_file(uploaded_file, include_date=False):
    """
    Carica una conversazione da un file di testo e verifica la sequenzialità temporale.
    Ogni messaggio deve rispettare l'ordine cronologico rispetto al precedente.

    Args:
        uploaded_file (UploadedFile): Il file caricato dall'utente.
        include_date (bool): Indica se i messaggi includono date e orari.

    Returns:
        tuple: Una lista di messaggi e la data associata (se presente).
    """
    messages = []
    last_message_time = None  # Teniamo traccia dell'ultimo timestamp per la verifica

    try:
        # Legge il contenuto del file
        content = uploaded_file.read().decode("utf-8").strip()
        lines = content.split("\n")

        for line in lines:
            # Parsing di ogni riga del file
            if include_date:
                try:
                    # Supponiamo che il formato sia "YYYY-MM-DD HH:MM:SS - Interlocutore: Messaggio"
                    date_part, rest = line.split(" - ", 1)
                    interlocutor, text = rest.split(": ", 1)

                    # Converte la stringa della data in un oggetto datetime
                    message_time = datetime.strptime(date_part, "%Y-%m-%d %H:%M:%S")

                    # Verifica della sequenzialità temporale
                    if last_message_time and message_time < last_message_time:
                        raise ValueError(
                            f"Errore di sequenzialità temporale: il messaggio '{line}' è fuori ordine."
                        )

                    last_message_time = message_time  # Aggiorna l'ultimo timestamp

                    # Aggiunge il messaggio
                    messages.append({
                        "date": date_part,
                        "interlocutor": interlocutor,
                        "text": text
                    })
                except ValueError as e:
                    raise ValueError(f"Errore durante il parsing della riga '{line}': {e}")
            else:
                # Formato senza date: "Interlocutore: Messaggio"
                interlocutor, text = line.split(": ", 1)

                # Assegna una data incrementale fittizia (utile per mantenere l'ordine)
                current_time = datetime.now()
                if last_message_time:
                    current_time = last_message_time + timedelta(seconds=1)  # Aggiunge un secondo
                last_message_time = current_time

                messages.append({
                    "date": current_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "interlocutor": interlocutor,
                    "text": text
                })

        # Determina la data generale della conversazione (prima data trovata)
        chat_date = messages[0]["date"] if messages else None
        return messages, chat_date
    except Exception as e:
        raise ValueError(f"Errore durante il caricamento del file: {e}")


# Funzione per generare un report della conversazione
def generate_report(conversation):
    """
    Genera un report basato sulla conversazione fornita.
    :param conversation: Lista di messaggi, ciascuno con "interlocutor", "text", e opzionalmente "date".
    :return: Una stringa con il report.
    """
    try:
        # Inizializza il report come stringa
        report = "Report della Conversazione\n\n"

        for message in conversation:
            # Estrai i dettagli dal dizionario
            date = message.get("date", "Data non specificata")
            speaker = message.get("interlocutor", "Interlocutore sconosciuto")
            text = message.get("text", "Messaggio vuoto")

            # Aggiungi i dettagli al report
            report += f"Data: {date}\n"
            report += f"{speaker}: {text}\n\n"

        # Restituisci il report completo
        return report.strip()

    except Exception as e:
        print(f"Errore durante la generazione del report: {e}")
        return None


def create_downloadable_file(content):
    return content.encode("utf-8")
