from datetime import datetime
import streamlit as st
from database import create_user, authenticate_user, init_db, save_report, fetch_reports
from utils import generate_pdf_report, load_chat_from_file
import os

# Inizializzazione del database se non esiste già
init_db()

# Configura la pagina di Streamlit
st.set_page_config(
    page_title="EmotionsRealeave",  # Titolo che appare nella scheda del browser
    page_icon="img/logo-nobg.png",  # Emoji o percorso dell'icona
    layout="centered",  # Può essere "centered" o "wide"
    initial_sidebar_state="expanded",  # Può essere "expanded", "collapsed" o "auto"
)

# Gestione dello stato del login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("Benvenuto nella Piattaforma di Analisi Emotiva: EmotionsReleave")

    # Opzioni di login e registrazione
    registration = st.radio("Scegli un'opzione:", ("Login", "Registrati"))

    if registration == "Registrati":
        st.subheader("Registrazione")
        username = st.text_input("Username", key="register_username")
        password = st.text_input("Password", type="password", key="register_password")
        confirm_password = st.text_input("Conferma Password", type="password", key="register_confirm_password")

        if st.button("Registrati"):
            if password == confirm_password:
                if create_user(username, password):
                    st.success("Registrazione riuscita! Ora puoi fare login.")
                else:
                    st.error("Username già in uso. Prova con un altro username.")
            else:
                st.error("Le password non coincidono.")

    elif registration == "Login":
        st.subheader("Login")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login"):
            if authenticate_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login effettuato con successo!")
            else:
                st.error("Username o password non validi.")

    # Blocca l'esecuzione se l'utente non è loggato
    st.stop()

# Se l'utente è loggato, mostra la schermata principale
st.sidebar.title(f"Benvenuto, {st.session_state.username}")
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.username = None
    st.rerun()

st.title("Analisi delle Emozioni")

# Inizializzazione dello stato dei messaggi
if "messages" not in st.session_state:
    st.session_state.messages = []

# Caricamento della conversazione
uploaded_file = st.file_uploader("Carica un file di testo", type=["txt"])
if uploaded_file:
    try:
        # Carica la chat dal file e traduci automaticamente in inglese per l'analisi
        chat, chat_date = load_chat_from_file(uploaded_file, include_date=True, translate_to_english=True)

        if chat:
            st.session_state.messages = chat
            st.success(f"Conversazione caricata con successo! Data della chat: {chat_date}")
        else:
            st.warning("Il file caricato non contiene messaggi validi.")
    except ValueError as e:
        st.error(f"Errore durante il caricamento: {e}")

# Visualizza la conversazione originale in italiano
st.subheader("Conversazione")
if len(st.session_state.messages) > 0:
    for msg in st.session_state.messages:
        st.write(f"{msg['date']} - {msg['interlocutor']}: {msg['text']}")
else:
    st.write("Nessun messaggio trovato.")

# Tasto per cancellare la conversazione
if st.button("Cancella Conversazione"):
    st.session_state.messages = []
    st.success("Conversazione cancellata!")

# Analisi delle emozioni e generazione del report
# Analisi delle emozioni e generazione del report
if st.button("Valuta la Conversazione", key="valuta_conversazione_button"):
    if len(st.session_state.messages) > 0:
        # Creazione del report basato sui messaggi (assicurati che restituisca bytes, non str)
        report_file = generate_pdf_report(st.session_state.messages)

        # Nome del file per il report con un formato valido
        report_name = f"report_{st.session_state.username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        print(f"Nome del report generato: {report_name}")
        report_path = os.path.join("reports", report_name)

        # Verifica se la cartella 'reports' esiste, altrimenti la crea
        if not os.path.exists("reports"):
            os.makedirs("reports")

        # Salva il file PDF nella cartella 'reports'
        with open(report_path, "wb") as f:  # Usa 'wb' per i file binari
            f.write(report_file)  # Scrivi i dati binari nel file

        # Salva il report nel database con il nome del file
        save_report(st.session_state.username, report_name)

        # Leggi il PDF in memoria per il download
        with open(report_path, "rb") as f:
            pdf_data = f.read()

        # Aggiungi il pulsante di download
        st.download_button(
            label="Scarica il Report",
            data=pdf_data,  # Usa i dati letti dal file temporaneo
            file_name=report_name,
            mime="application/pdf"
        )
    else:
        st.warning("Aggiungi dei messaggi prima di valutare la conversazione.")

# Sezione per visualizzare i report salvati
st.sidebar.subheader("I miei report")
reports = fetch_reports(st.session_state.username)

if reports:
    for report in reports:
        # Verifica che il percorso del report esista prima di aprirlo
        report_path = os.path.join("reports", report['path'])

        # Debug: Stampa il percorso del report
        print(f"Sto cercando il file: {report_path}")

        if os.path.exists(report_path):
            try:
                # Leggi il file PDF
                with open(report_path, "rb") as f:
                    pdf_data = f.read()

                # Aggiungi il pulsante di download
                st.sidebar.download_button(
                    label=f"Scarica Report - {report['timestamp']}",
                    data=pdf_data,
                    file_name=report['path'].split('/')[-1],
                    mime="application/pdf"
                )
            except Exception as e:
                st.sidebar.write(f"Errore nel leggere il report {report['timestamp']}: {e}")
        else:
            st.sidebar.write(f"Il report {report['timestamp']} non è stato trovato.")
else:
    st.sidebar.write("Nessun report disponibile.")
