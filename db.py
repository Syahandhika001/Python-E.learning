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

def initialize_database():
    conn = connect_db()
    cursor = conn.cursor()

    # Buat tabel users jika belum ada
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    ''')

    # Buat tabel reports jika belum ada
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            score INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # Buat tabel materi
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS materi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            judul TEXT NOT NULL,
            deskripsi TEXT
        )
    ''')

    # Buat tabel bahan_ajar, terhubung ke materi
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bahan_ajar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            materi_id INTEGER,
            nama_bahan TEXT NOT NULL,
            file_path TEXT,
            FOREIGN KEY (materi_id) REFERENCES materi (id)
        )
    ''')

    # Buat tabel questions, terhubung ke materi
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            materi_id INTEGER,
            question TEXT,
            option_a TEXT,
            option_b TEXT,
            option_c TEXT,
            option_d TEXT,
            correct_answer TEXT,
            explanation TEXT,
            FOREIGN KEY (materi_id) REFERENCES materi (id)
        )
    ''')

    conn.commit()
    conn.close()
