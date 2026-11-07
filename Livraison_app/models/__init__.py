import sqlite3
from werkzeug.security import check_password_hash

def connect():
    session = sqlite3.connect("Database.db")
    session.execute("PRAGMA foreign_keys = ON")
    return session

def init_database():
    session = connect()
    curseur = session.cursor()

    curseur.execute("""
    CREATE TABLE IF NOT EXISTS USERS(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NOM TEXT NOT NULL,
    PRENOM TEXT NOT NULL,
    MAIL TEXT UNIQUE NOT NULL,
    PASSWORD TEXT NOT NULL,
    ROLE TEXT NOT NULL DEFAULT 'commercant' CHECK (role IN ('commercant', 'livreur', 'admin')),
    DATE TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    )

    """)

    curseur.execute("""
    CREATE TABLE IF NOT EXISTS livraisons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        commercant_id INTEGER NOT NULL,
        livreur_id INTEGER,
        depart TEXT NOT NULL,
        arrivee TEXT NOT NULL,
        distance_km REAL NOT NULL CHECK (distance_km > 0),
        prix REAL NOT NULL CHECK (prix >= 0),
        statut TEXT NOT NULL DEFAULT 'en_attente' CHECK (statut IN ('en_attente', 'acceptee', 'en_cours', 'terminee', 'annulee')),
        date_creation TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (commercant_id) REFERENCES utilisateurs(id),
        FOREIGN KEY (livreur_id) REFERENCES utilisateurs(id)
    )
    """)

    session.commit()
    session.close()


    
def add_user(nom, prenom, mail,password):
    conn = connect()
    try:
        c = conn.cursor()
        c.execute(
            "INSERT INTO USERS (NOM, PRENOM, MAIL,PASSWORD) VALUES (?, ?, ?,?)",
            (nom, prenom, mail,password)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        conn.rollback()
        return False
    except sqlite3.Error as e:
        conn.rollback()
        print(f"Erreur SQLite : {e}")
        return False
    finally:
        conn.close()

def db_checking(mail,password):
    session = connect()
    curseur = session.cursor()

    curseur.execute ("SELECT NOM,PRENOM,MAIL,PASSWORD FROM USERS WHERE MAIL = ?" ,(mail,))


    user = curseur.fetchone()
    session.close()
    if user is None:
        return None

    if check_password_hash (user[3],password):
        return {
            "nom" : user[0],
            "prenom" : user[1],
            "mail" : user[2]
        }
    


def close_session(session):
    session.close()