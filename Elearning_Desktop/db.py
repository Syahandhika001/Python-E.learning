import sqlite3

# Fungsi untuk menghubungkan ke database SQLite
def connect_db():
    return sqlite3.connect("elearning.db")

# Fungsi untuk mendaftarkan user baru (register)
def register_user(username, password, role):
    """Fungsi untuk registrasi pengguna baru"""
    conn = connect_db()
    cursor = conn.cursor()

    # Pastikan tabel ada
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    ''')

    # Cek apakah username sudah ada
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()
        return False  # Username sudah ada

    # Masukkan data baru
    cursor.execute("""
        INSERT INTO users (username, password, role) 
        VALUES (?, ?, ?)
    """, (username, password, role))
    conn.commit()
    conn.close()
    return True
