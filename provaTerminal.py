import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F

# Caricamento del modello pre-addestrato GoEmotions

#bisogna mettere il nostro modello
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


# Streamlit UI
st.title("Classificatore di Emozioni in Conversazioni (GoEmotions)")
st.write("Inserisci una conversazione simulata per analizzare le emozioni associate a ciascun messaggio.")

# Cronologia della conversazione
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Input di messaggi in stile chat
user_input = st.text_input("Inserisci un messaggio:", placeholder="Scrivi qui il messaggio...")
speaker = st.selectbox("Seleziona l'interlocutore:", ["Interlocutore 1", "Interlocutore 2"])

if st.button("Aggiungi Messaggio"):
    if user_input.strip():
        st.session_state.conversation.append((speaker, user_input))
    else:
        st.warning("Per favore, inserisci un messaggio valido!")

# Mostra la conversazione
st.markdown("### Conversazione")
for speaker, message in st.session_state.conversation:
    st.markdown(f"**{speaker}:** {message}")

# Analizza la conversazione completa
if st.button("Valuta Conversazione"):
    st.markdown("### Analisi delle Emozioni")
    for speaker, message in st.session_state.conversation:
        emotion, confidence = classify_emotion(message)
        st.markdown(
            f"**{speaker}:** {message}  \n"
            f"**Emozione rilevata:** {emotion}  \n"
            f"**Confidenza:** {confidence:.2f}"
        )

st.markdown("---")
st.caption("Applicazione basata sul dataset GoEmotions e su un modello pre-addestrato di BERT.")
