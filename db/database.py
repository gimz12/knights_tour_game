import sqlite3

def connect_db():
    return sqlite3.connect("knight_game.db")

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS winners (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            method TEXT,
            sequence TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_winner(name, method, sequence):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO winners (name, method, sequence) VALUES (?, ?, ?)",
                   (name, method, str(sequence)))
    conn.commit()
    conn.close()
