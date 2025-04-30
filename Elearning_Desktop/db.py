import sqlite3



def connect_db():
    conn = sqlite3.connect("database.db")
    return conn

def init_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS  question(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL
        )
    ''')

    conn = sqlite3.connect("database.db") 
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    for row in cursor.fetchall():
        print(row)

    
    conn.commit()
    conn.close()

