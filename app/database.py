import sqlite3
from datetime import datetime

DB_PATH = "data/stato.db"


def connessione():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = connessione()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS sistema(
        totale_partiti INTEGER,
        totale_arrivati INTEGER
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS collegamenti(
        partenza TEXT,
        arrivo TEXT,
        ingresso TEXT
    )
    """)

    conn.commit()
    conn.close()

def init_sistema():
    conn = connessione()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM sistema")

    if cur.fetchone()[0] == 0:
        cur.execute(
            "INSERT INTO sistema VALUES (?, ?)",
            (0, 0)
        )

    conn.commit()
    conn.close()

def aggiungi_persona(collegamento, ora):
    conn = connessione()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO collegamenti
        VALUES (?, ?, ?)
        """,
        (
            collegamento.partenza.nome,
            collegamento.arrivo.nome,
            ora.isoformat()
        )
    )

    conn.commit()
    conn.close()