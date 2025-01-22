import streamlit as st
from database import create_user, authenticate_user, save_report, fetch_reports, init_db
from utils import generate_report, load_chat_from_file

# Inizializzazione del database se non esiste già
init_db()

# Gestione login/logout e registrazione
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Se l'utente è loggato, visualizza la schermata principale, altrimenti la schermata di login/registrazione
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
                # Registrazione dell'utente
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
            # Verifica del login
            if authenticate_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login effettuato con successo!")
            else:
                st.error("Username o password non validi")

    st.stop()  # Ferma l'esecuzione e impedisce di mostrare il resto della pagina finché non è loggato

# Se l'utente è loggato, mostra la schermata principale
st.sidebar.title(f"Benvenuto, {st.session_state.username}")
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.username = None
    st.rerun()  # Riavvia l'app per tornare alla schermata di login

# UI per aggiungere una chat manualmente o da file
st.title("Analisi delle Emozioni")
chat = ""

# Pulsante per scegliere se scrivere manualmente o caricare una conversazione
input_choice = st.radio("Scegli come inserire la conversazione", ("Scrivi Manualmente", "Carica da File"))

if input_choice == "Carica da File":
    uploaded_file = st.file_uploader("Carica un file di testo", type=["txt"])
    if uploaded_file:
        chat = load_chat_from_file(uploaded_file)
        if chat:  # Se la chat viene caricata correttamente
            st.session_state.messages = chat
            st.success("Conversazione caricata con successo!")
else:
    # Scrittura manuale della conversazione
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    interlocutor = st.selectbox("Scegli l'interlocutore", ["Interlocutore 1", "Interlocutore 2"])
    message = st.text_area("Scrivi un messaggio")

    if st.button("Aggiungi Messaggio"):
        if message:
            st.session_state.messages.append({"interlocutor": interlocutor, "text": message})
            st.success("Messaggio aggiunto!")

# Visualizza la conversazione
st.subheader("Conversazione")
if len(st.session_state.messages) > 0:
    for msg in st.session_state.messages:
        st.write(f"{msg['interlocutor']}: {msg['text']}")
else:
    st.write("Nessun messaggio trovato.")

# Analisi delle emozioni e generazione del report
if st.button("Valuta la Conversazione"):
    if len(st.session_state.messages) > 0:
        report = generate_report(st.session_state.messages)
        st.success("Report generato!")

        # Assicurati che report sia una stringa
        if isinstance(report, str):
            save_report(st.session_state.username, report)
        else:
            st.error("Il report generato non è una stringa valida.")
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
