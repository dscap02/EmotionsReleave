import os
import sqlite3

# Percorso al file del database
DB_PATH = "db/app_database.db"

# Funzione per connettersi al database
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Permette di accedere ai dati come dizionari
    return conn


# Funzione per creare la struttura iniziale del database
def init_db():
    # Crea la cartella 'db' se non esiste
    if not os.path.exists('db'):
        os.makedirs('db')

    conn = get_db_connection()
    cursor = conn.cursor()

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
    conn.close()
