import customtkinter as ctk
from db import connect_db
from Screens.login_screen import LoginApp
from screeninfo import get_monitors


class GuruApp(ctk.CTk):
    def __init__(self, user_id, previous_screen=None):
        super().__init__()
        self.title("Input Soal - Guru")
        self.set_fullscreen_windowed()
        self.user_id = user_id
        self.previous_screen = previous_screen

        self.ensure_column_materi_id_exists()
        self.create_widgets()

    def set_fullscreen_windowed(self):
        monitor = get_monitors()[0]
        self.geometry(f"{monitor.width}x{monitor.height}+0+0")

    def create_widgets(self):
        ctk.CTkLabel(self, text="Input Soal Pilihan Ganda", font=("Arial", 26)).place(relx=0.5, rely=0.06, anchor="center")

        # Pilih materi
        ctk.CTkLabel(self, text="Pilih Materi:").place(relx=0.2, rely=0.12, anchor="w")
        self.materi_option = ctk.CTkOptionMenu(self, values=self.get_materi_list())
        self.materi_option.place(relx=0.3, rely=0.12, anchor="w")

        # Input fields
        self.entries = {
            'question': ctk.CTkEntry(self, placeholder_text="Tulis soal di sini, contoh: 1 + 1 = ...?"),
            'a': ctk.CTkEntry(self, placeholder_text="Pilihan A"),
            'b': ctk.CTkEntry(self, placeholder_text="Pilihan B"),
            'c': ctk.CTkEntry(self, placeholder_text="Pilihan C"),
            'd': ctk.CTkEntry(self, placeholder_text="Pilihan D"),
            'correct': ctk.CTkEntry(self, placeholder_text="Jawaban Benar (misal: A)"),
            'explanation': ctk.CTkEntry(self, placeholder_text="Penjelasan Soal")
        }

        for i, entry in enumerate(self.entries.values()):
            entry.place(relx=0.5, rely=0.2 + i * 0.08, relwidth=0.6, relheight=0.05, anchor="center")

        self.status = ctk.CTkLabel(self, text="", font=("Arial", 14))
        self.status.place(relx=0.5, rely=0.8, anchor="center")

        ctk.CTkButton(self, text="Simpan Soal", command=self.simpan_soal).place(relx=0.4, rely=0.7, relwidth=0.18, relheight=0.07)
        ctk.CTkButton(self, text="Kembali", command=self.back_to_previous).place(relx=0.6, rely=0.7, relwidth=0.18, relheight=0.07)

    def ensure_column_materi_id_exists(self):
        try:
            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("PRAGMA table_info(questions)")
            columns = [col[1] for col in cursor.fetchall()]

            if "materi_id" not in columns:
                cursor.execute("ALTER TABLE questions ADD COLUMN materi_id INTEGER")
                conn.commit()

            conn.close()
        except Exception as e:
            print("Gagal memastikan kolom materi_id:", e)

    def get_materi_list(self):
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT id, judul FROM materi")
            rows = cursor.fetchall()
            conn.close()
            return [f"{id} - {judul}" for id, judul in rows] if rows else ["-"]
        except Exception as e:
            print("Gagal memuat materi:", e)
            return ["-"]

    def simpan_soal(self):
        materi_val = self.materi_option.get()
        if not materi_val or materi_val == "-":
            self.status.configure(text="Pilih materi terlebih dahulu!", text_color="red")
            return

        try:
            materi_id = int(materi_val.split(" - ")[0])
        except:
            self.status.configure(text="Format materi tidak valid!", text_color="red")
            return

        data = {key: entry.get().strip() for key, entry in self.entries.items()}

        if not data['question'] or data['question'].isdigit():
            self.status.configure(text="Soal harus berupa teks pertanyaan!", text_color="red")
            return

        if not all(data.values()):
            self.status.configure(text="Semua field harus diisi!", text_color="orange")
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO questions (materi_id, question, option_a, option_b, option_c, option_d, correct_answer, explanation)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                materi_id,
                data['question'], data['a'], data['b'], data['c'], data['d'],
                data['correct'].upper(),
                data['explanation']
            ))
            conn.commit()
            conn.close()

            self.status.configure(text="Soal berhasil disimpan!", text_color="green")
            for entry in self.entries.values():
                entry.delete(0, "end")

        except Exception as e:
            print("Gagal simpan soal:", e)
            self.status.configure(text="Terjadi kesalahan saat menyimpan!", text_color="red")

    def back_to_previous(self):
        self.destroy()
        if self.previous_screen:
            self.previous_screen.deiconify()

    def exit_to_login(self):
        self.destroy()
        LoginApp().mainloop()
