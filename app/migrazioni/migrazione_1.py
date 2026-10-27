import sys
from pathlib import Path

posizione_file = Path(__file__).resolve()
root_progetto = posizione_file.parent.parent
sys.path.append(str(root_progetto))


from data_base import get_connection

def migrazione_1(connessione):
    risultato_migrazione = connessione.executescript(
        """ 
            CREATE TABLE IF NOT EXISTS secco (
                id INTEGER PRIMARY KEY,
                nome_prodotto TEXT NOT NULL UNIQUE,
                scadenza TEXT,
                note TEXT DEFAULT 'non necessario',
                data_creazione CURRENT_TIMESTAMP
            );
            PRAGMA VERSION = 1;
        """
    )
    return 

def prova_selezione_secco(connessione):
    ricerca = connessione.execute(""" 
        SELECT * FROM secco;
        """
    )
    return [dict(riga) for riga in ricerca.fetchall()]


if __name__ == "__main__":
    connessione = get_connection()
    lancio_migrazione = migrazione_1(connessione)
    prova = prova_selezione_secco(connessione)
    print(prova)
    
    