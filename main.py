import streamlit as st
from database import create_user, authenticate_user, save_report, fetch_reports, init_db
from utils import generate_report, load_chat_from_file
from datetime import datetime

# Inizializzazione del database se non esiste già
init_db()

# Gestione login/logout e registrazione
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("Benvenuto nella Piattaforma di Analisi Emotiva")

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
                st.error("Username o password non validi")

    st.stop()  # Ferma l'esecuzione se non loggato

# Se l'utente è loggato, mostra la schermata principale
st.sidebar.title(f"Benvenuto, {st.session_state.username}")
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.username = None
    st.rerun()

st.title("Analisi delle Emozioni")
chat = ""

# UI per inserire la conversazione
input_choice = st.radio("Scegli come inserire la conversazione", ("Scrivi Manualmente", "Carica da File"))

if 'messages' not in st.session_state:
    st.session_state.messages = []

if input_choice == "Carica da File":
    uploaded_file = st.file_uploader("Carica un file di testo", type=["txt"])
    if uploaded_file:
        try:
            chat, chat_date = load_chat_from_file(uploaded_file, include_date=True)
            if chat:
                st.session_state.messages = chat
                st.success(f"Conversazione caricata con successo! Data della chat: {chat_date}")
            else:
                st.warning("Il file caricato non contiene messaggi validi.")
        except ValueError as e:
            st.error(f"Errore durante il caricamento: {e}")
else:
    st.subheader("Scrivi la conversazione manualmente")
    interlocutor = st.selectbox("Scegli l'interlocutore", ["Interlocutore 1", "Interlocutore 2"])
    message = st.text_area("Scrivi un messaggio")
    date_input = st.date_input("Data del messaggio", datetime.now().date())
    time_input = st.time_input("Orario del messaggio", datetime.now().time())

    if st.button("Aggiungi Messaggio"):
        if message:
            # Costruisci il timestamp completo
            message_datetime = datetime.combine(date_input, time_input)
            # Controlla la sequenzialità temporale
            if st.session_state.messages and datetime.strptime(
                    st.session_state.messages[-1]["date"], "%Y-%m-%d %H:%M:%S") > message_datetime:
                st.error("Il messaggio non rispetta l'ordine cronologico della conversazione!")
            else:
                st.session_state.messages.append({
                    "date": message_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                    "interlocutor": interlocutor,
                    "text": message
                })
                st.success("Messaggio aggiunto!")

# Visualizza la conversazione
st.subheader("Conversazione")
if len(st.session_state.messages) > 0:
    for msg in st.session_state.messages:
        st.write(f"{msg['date']} - {msg['interlocutor']}: {msg['text']}")
else:
    st.write("Nessun messaggio trovato.")

# Analisi delle emozioni e generazione del report
if st.button("Valuta la Conversazione"):
    if len(st.session_state.messages) > 0:
        try:
            report = generate_report(st.session_state.messages)
            st.success("Report generato!")
            st.download_button("Scarica Report", data=report, file_name="report.txt", mime="text/plain")
            save_report(st.session_state.username, report)
        except Exception as e:
            st.error(f"Errore durante la generazione del report: {e}")
    else:
        st.error("Nessun messaggio nella conversazione!")

# Visualizza i report salvati
st.sidebar.title("I tuoi Report")
for report in fetch_reports(st.session_state.username):
    st.sidebar.markdown(f"- {report['timestamp']} [Scarica]({report['path']})")

# Pulsante per cancellare la conversazione
if st.button("Cancella Conversazione"):
    st.session_state.messages = []
    st.success("Conversazione cancellata!")
