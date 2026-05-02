import sqlite3

def get_db_connection():
    # Connects to a local SQLite file
    conn = sqlite3.connect("stocks.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    # Create table for monthly data
    conn.execute('''
        CREATE TABLE IF NOT EXISTS monthly_data (
        symbol TEXT,
        date TEXT,
        high REAL,
        low REAL,
        volume INTEGER,
        PRIMARY KEY (symbol, date)
        )
    ''')
    conn.commit()
    conn.close()

def read_annual_data_from_db(symbol: str, year: str, conn):
    cursor = conn.execute(
        "SELECT * FROM monthly_data WHERE symbol = ? AND date LIKE ?", 
        (symbol, f"{year}%")
    )
    rows = cursor.fetchall()
    return rows