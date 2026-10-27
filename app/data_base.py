"""
    Questo file si occupa principalmente di costruire le cartelle / sotto cartelle / file sqlite / aprire la connessione / settare le regole di base del DB
"""
import sqlite3
import os
from pathlib import Path

#Root progetto
root_progetto = Path(__file__).resolve().parent
#Path root + catella
cartella_db = root_progetto/"database"
#Nome del file
nome_db = "db_frigo.db"
#Creo la cartella / se esiste non do errore
os.makedirs(cartella_db, exist_ok=True)

#Creo il file con join
percorso_db = os.path.join(cartella_db,nome_db)

def get_connection():
    #Apro la connessione verso il file
    connessione = sqlite3.connect(percorso_db)
    #Aggiungo modalita WAL
    connessione.execute("PRAGMA journal_mode=WAL;")
    connessione.execute("PRAGMA foreign_key=ON;")
    return connessione


if __name__ == "__main__":    
    #Creazione della connessione
    connessione = get_connection()
    try:
        #Controllo che il file esista sul disco
        if os.path.exists(cartella_db/nome_db):
            print(f"Il database è stato creato in questo punto -> {percorso_db}")
        else:
            print("Il db non esiste")
    finally:
        connessione.close()
        
    #Versione PRAGMA
    connessione = get_connection()
    try:
        versione = connessione.execute(
                "PRAGMA user_version;"
            ).fetchone()[0]
        print("Versione", versione)
    finally:
        connessione.close()
    
    
    