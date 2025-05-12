import sqlite3

# Fungsi untuk koneksi ke database
def connect_db():
    return sqlite3.connect("elearning.db")

# Fungsi untuk inisialisasi tabel-tabel di database
def init_db():
    conn = connect_db()
    cursor = conn.cursor()

    # Tabel pengguna
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('siswa', 'guru'))
        )
    ''')

    # Tabel soal
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            option_d TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            explanation TEXT NOT NULL
        )
    ''')

    # Tabel jawaban siswa
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            question_id INTEGER,
            answer TEXT NOT NULL,
            correct INTEGER NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(question_id) REFERENCES questions(id)
        )
    ''')

    # Tabel laporan nilai siswa
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            user_id INTEGER PRIMARY KEY,
            score INTEGER NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()
