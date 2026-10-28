"""
    Questo file si occupa principalmente di costruire le cartelle / sotto cartelle / file sqlite / aprire la connessione / settare le regole di base del DB
"""
import sqlite3
import os
from pathlib import Path
from typing import Any,Optional

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

#La versione del clock interno di sqlite
schema_version = 1

#BLocco funzioni di supporto -> in questo caso non dovrebbero serire, perchè ho aggiunto row_factory
#Funzioni di supporto al database 
def row_to_dict(row: Optional[sqlite3.Row]) -> Optional[dict[str, Any]]:
    return dict(row) if row is not None else None

def row_to_dict_leggibile(row: sqlite3.Row):
    if row is not None:
        return dict(row)
    else:
        return None


def rows_to_dicts(rows: list[sqlite3.Row]) -> list[dict[str, Any]]:
    return [dict(row) for row in rows]

def rows_to_dicts_leggibile(rows: sqlite3.Row):
    #Lista vuota
    lista_dizionari = []
    #Per ogni singolo elemento 
    for row in rows:
        #Trasformo il singolo elemento in un dizionario
        dizionario = dict(row)
        #Lo metto nella lista vuota
        lista_dizionari.append(dizionario)
    #Torno una lista di dizionari   
    return lista_dizionari


#connessione database ( collegamento fisico )
def get_connection() -> sqlite3.Connection:
    #Apro la connessione verso il file
    connessione = sqlite3.connect(percorso_db)
    
    #Output database in formato dizionario e non tuple 
    connessione.row_factory = sqlite3.Row
    #Garantisco l'integrita tra le tabelle
    connessione.execute("PRAGMA foreign_keys = ON;")
    connessione.execute("PRAGMA synchonous = NORMAL;")
    
    return connessione 

#Prima migrazione, agginugo una tabella relativa al compartimento del secco
# nome tabella -> sezione_secco
# colonne -> 
# nome_prodotto (id,testo,unico), 
# data_acquisto(data <= scadenza_prodotto), 
# scadenza_prodotto(data >= data_acquisto), 
# codice_barre(intero,almeno 10 numeri) 

def tabella_freschi():
    schema_sql = f""" 
        CREATE TABLE IF NOT EXISTS sezione_freschi(
            id INTEGER PRIMARY KEY,
            nome_prodotto TEXT NOT NULL UNIQUE
                CHECK (length(trim(nome_prodotto))>0),
            data_acquisto TEXT NOT NULL,
            data_scadenza TEXT NOT NULL,
            note TEXT DEFAULT '',
            attivo INTEGER NOT NULL DEFAULT 1
                CHECK (attivo IN (0,1)),
              
            inserito_il TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP      
        );    
        """
    
    connessione = get_connection()
    try:
        with connessione:
            #Leggo la versione attuale
            current_version = connessione.execute("PRAGMA user_version").fetchone()[0]
            if current_version < 2:
                cursore = connessione.execute(schema_sql)
                #Aggiorno i due contatori 
                current_version = connessione.execute("PRAGMA user_version = 2")
                schema_version = 2

    finally:
        connessione.close()
        
def inizio_struttura_database() -> None:
    schema_sql = f""" 

        CREATE TABLE IF NOT EXISTS sezione_secco(
            id INTEGER PRIMARY KEY,
            
            nome_prodotto TEXT NOT NULL UNIQUE
                CHECK (length(trim(nome_prodotto)) > 0),
            
            data_acquisto TEXT NOT NULL,
            
            data_scadenza TEXT NOT NULL,
            
            note TEXT DEFAULT '',
            
            attivo INTEGER NOT NULL DEFAULT 1
                CHECK (attivo IN (0,1)),
                
            inserito_il TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT
        );    
    """
    
    connessione = get_connection()
    try:
        with connessione:
            #Estrapolo la versione attuale
            current_version = connessione.execute("PRAGMA user_version;").fetchone()[0]
            
            if current_version < 1:
                
                connessione.execute(schema_sql)
                #Subito dopo aggiorno la versione e la poro a 1
                connessione.execute("PRAGMA user_version = 1")
                
                #aggiorno l mio contatore
                schema_version = 1
    finally:
        connessione.close()
    


if __name__ == "__main__":    
    
    #Prima migrazione struttura iniziale con la sezione dei secchi
    try:
        #Lancio la prima migrazione
        inizio_struttura_database()
    except Exception as error:
        print(f"Migrazione non riuscita per il seguente motivo {error}")
    
    #Seconda migrazione -> aggiunto sezione freschi
    try:
        connessione = get_connection()
        tabella_freschi()
        print("Seconda migrazione effettuata")
    except Exception as error:
        print(f"Il Db è in errore {error}")
    
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
    
    
    #Prova lettura creazione corretta tabella
    connessione = get_connection()
    try:
        cursore = connessione.execute(
            "SELECT * FROM sezione_secco;"
        )
        print(f"Tabella {cursore.fetchall()}")
    except Exception as error:
        print(f"Errore {error}")

    #Provo a leggere la sezione freschi
    connessione = get_connection()
    try:
        cursore = connessione.execute(
            "SELECT * FROM sezione_freschi;"
        )
        print(f"Tabella Freschi {cursore.fetchall()}")
    except Exception as Errore:
        print(f"Tabella non riconosciuta o inesistente {Errore}")