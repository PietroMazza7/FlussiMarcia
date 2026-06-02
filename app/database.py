import sqlite3
from datetime import datetime, timedelta

DB_PATH = "data/stato.db"

def connessione():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = connessione()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS sistema(
        id INTEGER PRIMARY KEY CHECK (id = 1),
        totale_partiti INTEGER,
        totale_arrivati INTEGER
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS collegamenti(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
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

    cur.execute("SELECT COUNT(*) as c FROM sistema")
    if cur.fetchone()["c"] == 0:
        cur.execute("""
            INSERT INTO sistema (id, totale_partiti, totale_arrivati)
            VALUES (1, 0, 0)
        """)

    conn.commit()
    conn.close()

def aggiungi_persona(collegamento, ora: datetime):
    conn = connessione()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO collegamenti (partenza, arrivo, ingresso)
        VALUES (?, ?, ?)
    """, (
        collegamento.partenza.nome,
        collegamento.arrivo.nome,
        ora.isoformat()
    ))

    conn.commit()
    conn.close()

def conta_collegamento(collegamento) -> int:
    conn = connessione()
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*) as c
        FROM collegamenti
        WHERE partenza = ? AND arrivo = ?
    """, (collegamento.partenza, collegamento.arrivo))

    val = cur.fetchone()["c"]
    conn.close()
    return val

def arrivi_entro_collegamento(collegamento, ora: datetime, minuti: int) -> int:
    soglia = ora + timedelta(minutes=minuti)

    conn = connessione()
    cur = conn.cursor()

    cur.execute("""
        SELECT ingresso
        FROM collegamenti
        WHERE partenza = ? AND arrivo = ?
    """, (collegamento.partenza, collegamento.arrivo))

    rows = cur.fetchall()
    conn.close()

    return sum(
        datetime.fromisoformat(r["ingresso"]) + timedelta(minutes=collegamento.tempo) <= soglia
        for r in rows
    )

def rimuovi_piu_vecchio(collegamento, peek: bool = False):
    conn = connessione()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, ingresso
        FROM collegamenti
        WHERE partenza = ? AND arrivo = ?
        ORDER BY ingresso ASC
        LIMIT 1
    """, (collegamento.partenza, collegamento.arrivo))

    row = cur.fetchone()

    if not row:
        conn.close()
        return None

    if peek:
        conn.close()
        return datetime.fromisoformat(row["ingresso"])

    cur.execute("""
        DELETE FROM collegamenti
        WHERE id = ?
    """, (row["id"],))

    conn.commit()
    conn.close()

    return datetime.fromisoformat(row["ingresso"])