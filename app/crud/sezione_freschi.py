from pathlib import Path
import sys
import sqlite3

# Aiuto python a cercare la root del progetto per importare meglio le funzioni
path_questo_file = Path(__file__).resolve()
root_progetto = path_questo_file.parent.parent
sys.path.append(str(root_progetto))

from data_base import get_connection
from data_base import rows_to_dicts_leggibile

"""   
    In questo documento vado a inserire le prime CRUD per la sezione dei freschi
    Per il momento inserisco 4 funzioni di base :
    -Definisci un nuovo alimento
    -Elimina l'intero catalogo caricato
    -Mostra tutti gli elementi presenti
    -Eventualmente cancellare solo un dato prodotto caricato

"""

def inserisci_alimento(connessione,nome_prodotto,data_acquisto,data_scadenza,note):
    with connessione:
        cursore = connessione.execute(""" 
        INSERT INTO sezione_freschi (
        nome_prodotto,
        data_acquisto,
        data_scadenza,
        note)
        VALUES (?,?,?,?) 
        """,(nome_prodotto,data_acquisto,data_scadenza,note))
    return cursore.rowcount

def alimenti_caricati(connessione):
    with connessione:
        cursore = connessione.execute(""" 
            SELECT * FROM sezione_freschi;
        """)
    return cursore.fetchall()


if __name__ == "__main__":
    
    # try:
    #     connessione = get_connection()
    #     inseriscoAlimentoSezioneFreschi = inserisci_alimento(
    #         connessione,
    #         nome_prodotto="Grana Padano",
    #         data_acquisto="2026-01-01",
    #         data_scadenza="2026-01-15",
    #         note="Ancora non aperto"
    #     )
    #     print(f"Inserimento completato, {inseriscoAlimentoSezioneFreschi}")
    # except sqlite3.IntegrityError as errore:
    #     print(f"Operazione non riuscita, stai violando una condizione strutturale del database. {errore}")

    try:
        connessione = get_connection()
        risultati = alimenti_caricati(connessione)
        risultati_convertiti = rows_to_dicts_leggibile(risultati)

        for lista in risultati_convertiti:
            print(f'Nome prodotto {lista["nome_prodotto"]}')
            print(f'Scadenza {lista["data_scadenza"]}.')

    finally:
        connessione.close()

