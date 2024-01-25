import sqlite3

def create_users_table():
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            uid TEXT PRIMARY KEY,
            email TEXT,
            first_name TEXT,
            last_name TEXT,
            gender TEXT,
            latitude REAL,
            longitude REAL,
            datetime TEXT
        )
    ''')
    conn.commit()
    conn.close()
