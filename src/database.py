import sqlite3

conn = sqlite3.connect("solana.db")

def create_table():

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        signature TEXT,
        slot INTEGER,
        block_time INTEGER
    )
    """)

    conn.commit()


def insert_tx(signature, slot, block_time):

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO transactions (signature, slot, block_time)
    VALUES (?, ?, ?)
    """, (signature, slot, block_time))

    conn.commit()