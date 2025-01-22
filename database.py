import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import streamlit as st  # Correzione dell'importazione

# Percorso al file del database
DB_PATH = "db/app_database.db"


# Funzione per connettersi al database
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Permette di accedere ai dati come dizionari
    return conn


# Creazione dell'utente (registrazione)
def create_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Hash della password
    hashed_password = generate_password_hash(password)

    try:
        # Verifica che l'utente non esista già
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            return False  # L'username esiste già

        # Inserimento dell'utente
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()  # Se c'è un errore, annulliamo la transazione
        print(f"Errore durante la registrazione: {e}")
        return False
    finally:
        conn.close()

    return True  # Registrazione riuscita


# Funzione di login (verifica utente e password)
def authenticate_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Ricerca l'utente nel database
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        if user and check_password_hash(user['password'], password):
            return True
    except sqlite3.Error as e:
        print(f"Errore durante il login: {e}")
    finally:
        conn.close()

    return False


# Funzione per salvare un report
def save_report(username, report):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Verifica che la cartella 'reports' esista, altrimenti la crea
    if not os.path.exists("reports"):
        os.makedirs("reports")

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Inserimento del report nel database
        cursor.execute(
            "INSERT INTO reports (username, report, timestamp) VALUES (?, ?, ?)",
            (username, report, timestamp)
        )
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()  # Annulla la transazione in caso di errore
        print(f"Errore nel salvataggio del report: {e}")
    finally:
        conn.close()


# Funzione per ottenere i report salvati da un utente
def fetch_reports(username):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Recupera i report associati all'utente
        cursor.execute("SELECT * FROM reports WHERE username = ?", (username,))
        reports = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Errore nel recupero dei report: {e}")
        reports = []
    finally:
        conn.close()

    # Restituisce i report come lista di dizionari
    return [{'timestamp': report['timestamp'], 'path': f"reports/{report['timestamp']}.pdf"} for report in reports]


# Funzione per creare la struttura iniziale del database
def init_db():
    # Crea la cartella 'db' se non esiste
    if not os.path.exists('db'):
        os.makedirs('db')

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Creazione della tabella utenti
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        """)

        # Creazione della tabella per i report
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                report TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Errore nella creazione del database: {e}")
    finally:
        conn.close()
