import asyncio
from collections import Counter

import pandas as pd
import torch
from googletrans import Translator
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Caricamento del modello e del tokenizer del modello pre-addestrato (il modello BERT specificato)
MODEL_NAME = "bert_emotion_model"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=28)

# Imposta il dispositivo
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Mappa emozioni
emotion_dict = {
    0: 'ammirazione',
    2: 'rabbia',
    6: 'confusione',
    10: 'disapprovazione',
    11: 'disgusto',
    14: 'paura',
    17: 'gioia',
    25: 'tristezza',
    27: 'neutra'
}

# Funzione aggiornata per la classificazione
def classify_emotion(text):
    """
    Classifica l'emozione di un testo.
    :param text: Il testo da classificare
    :return: Una tupla (emozione, confidenza)
    """
    import emoji
    text = emoji.demojize(text)  # Converti le emoji in testo
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    # Predizione
    outputs = model(**inputs)
    probabilities = torch.nn.functional.softmax(outputs.logits, dim=1)
    max_index = torch.argmax(probabilities, dim=1).item()

    # Mappa l'indice predetto all'emozione ridotta
    if max_index in emotion_dict:
        emotion = emotion_dict[max_index]
    else:
        print(f"Errore: l'indice predetto {max_index} è fuori dal range delle emozioni ridotte.")
        emotion = 'neutra'  # Valore di fallback

    confidence = probabilities[0, max_index].item()
    return emotion, confidence


# Funzione per caricare la chat da un file

async def translate_text_async(text, src='it', dest='en'):
    """Traduzione asincrona del testo."""
    translator = Translator()
    translated = await translator.translate(text, src=src, dest=dest)
    return translated.text

def load_chat_from_file(uploaded_file, include_date=False, translate_to_english=False):
    """
    Carica una conversazione da un file di testo, verifica la sequenzialità temporale e, se richiesto, traduce i messaggi in inglese.
    Ogni messaggio deve rispettare l'ordine cronologico rispetto al precedente.
    """
    messages = []
    last_message_time = None  # Teniamo traccia dell'ultimo timestamp per la verifica
    translator = Translator()  # Inizializza il traduttore

    try:
        print("Inizio caricamento file chat...")
        # Legge il contenuto del file
        content = uploaded_file.read().decode("utf-8").strip()

        # Verifica se il file è vuoto
        if not content:
            raise ValueError("Il file caricato è vuoto.")

        lines = content.split("\n")

        for line in lines:
            # Salta le righe vuote
            if not line.strip():
                continue

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

                    # Se la traduzione è richiesta, traduco il messaggio
                    if translate_to_english:
                        translated_text = asyncio.run(translate_text_async(text, src='it', dest='en'))
                        #print(f"Messaggio originale: {text}")
                        #print(f"Tradotto: {translated_text}")
                    else:
                        translated_text = text  # Mantieni il testo originale in italiano
                        #print(f"Messaggio originale (no traduzione): {text}")

                    # Aggiunge il messaggio
                    messages.append({
                        "date": date_part,
                        "interlocutor": interlocutor,
                        "text": text,  # Salviamo il testo originale
                        "translated_text": translated_text  # Salviamo la traduzione per l'elaborazione
                    })
                except ValueError as e:
                    raise ValueError(f"Errore durante il parsing della riga '{line}': {e}")
            else:
                # Formato senza date: "Interlocutore: Messaggio"
                try:
                    interlocutor, text = line.split(": ", 1)
                except ValueError:
                    # Salta le righe malformate
                    continue

                # Assegna una data incrementale fittizia (utile per mantenere l'ordine)
                current_time = datetime.now()
                if last_message_time:
                    current_time = last_message_time + timedelta(seconds=1)  # Aggiunge un secondo
                last_message_time = current_time

                # Se la traduzione è richiesta, traduco il messaggio
                if translate_to_english:
                    translated_text = asyncio.run(translate_text_async(text, src='it', dest='en'))
                    #print(f"Messaggio originale: {text}")
                    #print(f"Tradotto: {translated_text}")
                else:
                    translated_text = text  # Mantieni il testo originale in italiano
                    #print(f"Messaggio originale (no traduzione): {text}")

                messages.append({
                    "date": current_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "interlocutor": interlocutor,
                    "text": text,  # Salviamo il testo originale
                    "translated_text": translated_text  # Salviamo la traduzione per l'elaborazione
                })

        # Verifica che ci siano effettivamente dei messaggi
        if not messages:
            raise ValueError("Nessun messaggio trovato nella conversazione.")

        # Determina la data generale della conversazione (prima data trovata)
        chat_date = messages[0]["date"] if messages else None
        print("Caricamento chat completato!")
        return messages, chat_date
    except Exception as e:
        raise ValueError(f"Errore durante il caricamento del file: {e}")


import torch
from datetime import datetime, timedelta

# Altre importazioni e variabili di configurazione
# ...

import os
import tempfile
import matplotlib.pyplot as plt
from fpdf import FPDF


def generate_pdf_report(conversation):
    try:
        if not conversation:
            raise ValueError("La conversazione non contiene messaggi.")

        print("Inizio generazione report PDF...")

        # Configurazione PDF
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.add_font('DejaVu', '', 'ttf/DejaVuSans.ttf', uni=True)
        pdf.add_font('DejaVu', 'B', 'ttf/DejaVuSans-Bold.ttf', uni=True)
        pdf.add_font('DejaVu', 'I', 'ttf/DejaVuSans-Oblique.ttf', uni=True)
        pdf.set_font("DejaVu", "", 12)  # Normale

        # Aggiungi il logo
        logo_path = "img/logo.jpg"  # Percorso del logo
        try:
            pdf.image(logo_path, x=80, w=50)  # Centra il logo (x=80 per centratura su una pagina A4)
        except Exception as e:
            print(f"Errore nel caricamento del logo: {e}")
            raise ValueError("Il file del logo non è stato trovato o non è accessibile.")

        # Titolo del Report
        pdf.ln(10)  # Spazio dopo il logo
        pdf.set_font("DejaVu", "B", 14)  # Grassetto
        pdf.cell(200, 10, txt="Report di Analisi delle Emozioni", ln=True, align="C")
        pdf.ln(10)

        # Testo introduttivo
        pdf.set_font("DejaVu", "", 12)  # Normale
        pdf.multi_cell(0, 10, txt="In questo report, vengono analizzate le emozioni rilevate nella conversazione.")
        pdf.ln(10)

        # Panoramica della Conversazione
        pdf.set_font("DejaVu", "B", 12)
        pdf.cell(200, 10, txt="1. Panoramica della Conversazione", ln=True)
        pdf.set_font("DejaVu", "", 12)

        total_messages = len(conversation)
        emotion_dict = {
            0: 'ammirazione', 2: 'rabbia', 6: 'confusione', 10: 'disapprovazione',
            11: 'disgusto', 14: 'paura', 17: 'gioia', 25: 'tristezza', 27: 'neutra'
        }
        emotions_list = list(emotion_dict.values())

        emotions_count = {emotion: 0 for emotion in emotions_list}  # Inizializza emozioni
        emotions_over_time = {}

        print(f"Totale messaggi: {total_messages}")

        for msg_index, msg in enumerate(conversation):
            try:
                # Usa il testo tradotto per l'analisi delle emozioni
                cleaned_text = msg.get('translated_text', '').strip().replace('\r', '').replace('\n', '')
                if not cleaned_text:
                    print(f"Messaggio {msg_index + 1}: Vuoto o solo spazi, ignorato.")
                    continue
                emotion, confidenza = classify_emotion(cleaned_text)  # Funzione aggiornata
                if emotion is None:
                    print(f"Messaggio {msg_index + 1}: Emozione non rilevata.")
                    continue

                emotions_count[emotion] += 1
                date = msg.get("date")
                if date not in emotions_over_time:
                    emotions_over_time[date] = []
                emotions_over_time[date].append(emotion)
            except Exception as e:
                print(f"Errore nell'elaborazione del messaggio {msg_index + 1}: {e}")

        if not any(emotions_count.values()):
            raise ValueError("Non sono state rilevate emozioni nei messaggi analizzati.")

        print(f"Conteggio emozioni: {emotions_count}")

        # Analisi emozioni più frequente e meno frequente
        try:
            most_common_emotion = max(emotions_count, key=emotions_count.get)
            least_common_emotion = min((e for e in emotions_count if emotions_count[e] > 0), key=emotions_count.get)
        except ValueError as e:
            print(f"Errore nell'analisi delle emozioni più e meno frequenti: {e}")
            most_common_emotion, least_common_emotion = "N/A", "N/A"

        neutral_percentage = (emotions_count.get('neutra', 0) / total_messages) * 100

        print(f"Emozione più frequente: {most_common_emotion}")
        print(f"Emozione meno frequente: {least_common_emotion}")
        print(f"Percentuale di messaggi neutri: {neutral_percentage:.2f}%")

        # Scrittura dei dati nel PDF
        pdf.multi_cell(0, 10, txt=f"- Numero totale di messaggi analizzati: {total_messages}")
        pdf.multi_cell(0, 10, txt=f"- Emozione più frequente: {most_common_emotion}")
        pdf.multi_cell(0, 10, txt=f"- Emozione meno frequente: {least_common_emotion}")
        pdf.multi_cell(0, 10, txt=f"- Percentuale di messaggi neutri: {neutral_percentage:.2f}%")
        pdf.ln(10)

        # Distribuzione delle Emozioni
        pdf.set_font("DejaVu", "B", 12)
        pdf.cell(200, 10, txt="2. Distribuzione delle Emozioni", ln=True)
        pdf.set_font("DejaVu", "", 12)
        pdf.multi_cell(0, 10, txt="La distribuzione delle emozioni nei messaggi analizzati è rappresentata di seguito.")
        pdf.ln(5)

        # Tabella delle Frequenze
        pdf.set_font("DejaVu", "B", 12)
        pdf.cell(95, 10, "Emozione", border=1, align='C')
        pdf.cell(95, 10, "Conteggio", border=1, align='C')
        pdf.ln()

        pdf.set_font("DejaVu", "", 12)
        for emotion, count in emotions_count.items():
            if count > 0:  # Escludi emozioni con frequenza 0
                pdf.cell(95, 10, emotion, border=1)
                pdf.cell(95, 10, str(count), border=1)
                pdf.ln()

        # Tendenze temporali
        pdf.set_font("DejaVu", "B", 12)
        pdf.cell(200, 10, txt="3. Tendenze Temporali delle Emozioni", ln=True)
        pdf.set_font("DejaVu", "", 12)
        pdf.multi_cell(0, 10, txt="Le tendenze temporali delle emozioni sono mostrate di seguito.")
        pdf.ln(5)

        # Crea DataFrame per analizzare le tendenze
        df = pd.DataFrame({
            'date': list(emotions_over_time.keys()),
            'emotion': [', '.join(v) for v in emotions_over_time.values()]
        })

        chart_filename = os.path.join(tempfile.gettempdir(), "emotion_trends.png")
        emotion_counts_over_time = df['emotion'].value_counts()
        plt.figure(figsize=(10, 6))
        emotion_counts_over_time.plot(kind='bar')
        plt.title('Emozioni nel Tempo')
        plt.ylabel('Conteggio')
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Salva il grafico come immagine
        chart_filename = os.path.join(tempfile.gettempdir(), "emotion_trends.png")
        plt.savefig(chart_filename)
        plt.close()

        # Aggiungi il grafico al PDF
        pdf.image(chart_filename, x=10, w=180)

        # Emozioni Predominanti per Giorno
        pdf.set_font("DejaVu", "B", 12)
        pdf.cell(200, 10, txt="4. Emozioni Predominanti per Giorno", ln=True)
        pdf.set_font("DejaVu", "", 12)

        # Crea una tabella per le emozioni predominanti giornaliere
        pdf.set_font("DejaVu", "B", 12)
        pdf.cell(95, 10, "Data", border=1, align='C')
        pdf.cell(95, 10, "Emozione Predominante", border=1, align='C')
        pdf.ln()

        for date, emotions in emotions_over_time.items():
            common_emotion = Counter(emotions).most_common(1)[0][0]
            pdf.set_font("DejaVu", "", 12)
            pdf.cell(95, 10, str(date), border=1)
            pdf.cell(95, 10, common_emotion, border=1)
            pdf.ln()

        # Salvataggio del PDF in un buffer di memoria
        pdf_output = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        pdf.output(pdf_output.name)

        # Leggi il file PDF generato in modalità binaria
        with open(pdf_output.name, 'rb') as f:
            pdf_data = f.read()

        return pdf_data

    except Exception as e:
        print(f"Errore nella generazione del report PDF: {e}")
        raise e
