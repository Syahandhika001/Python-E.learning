import customtkinter as ctk
import sqlite3
from db import register_user, connect_db


# Fungsi pindah ke halaman login
def exit_to_login(app):
    app.destroy()
    login_app = LoginApp()
    login_app.mainloop()


# Halaman Login
class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Halaman Login")
        self.geometry("300x330")
        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self, text="Masuk Akun").pack(pady=10)

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=10)

        ctk.CTkButton(self, text="Login", command=self.login).pack(pady=20)

        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.pack()

        ctk.CTkButton(self, text="Belum punya akun? Daftar di sini",
                      command=self.open_register, fg_color="transparent",
                      text_color="blue", hover_color="#ccc", border_width=1).pack(pady=10)

    def open_register(self):
        self.destroy()
        register_app = RegisterApp()
        register_app.mainloop()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            user = cursor.fetchone()
            conn.close()

            if user:
                user_id, role = user[0], user[3]
                self.destroy()
                if role == "guru":
                    GuruApp(user_id).mainloop()
                else:
                    SiswaApp(user_id).mainloop()
            else:
                self.status_label.configure(text="Username atau Password salah!", text_color="red")
        else:
            self.status_label.configure(text="Isi semua data!", text_color="orange")


# Halaman Guru
class GuruApp(ctk.CTk):
    def __init__(self, user_id):
        super().__init__()
        self.title("Guru - Input Soal")
        self.geometry("400x600")
        self.user_id = user_id
        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self, text="Input Soal Pilihan Ganda (Guru)").pack(pady=10)

        self.entries = {
            'question': ctk.CTkEntry(self, placeholder_text="Tulis soal di sini", width=300),
            'a': ctk.CTkEntry(self, placeholder_text="Pilihan A", width=300),
            'b': ctk.CTkEntry(self, placeholder_text="Pilihan B", width=300),
            'c': ctk.CTkEntry(self, placeholder_text="Pilihan C", width=300),
            'd': ctk.CTkEntry(self, placeholder_text="Pilihan D", width=300),
            'correct': ctk.CTkEntry(self, placeholder_text="Jawaban Benar", width=300),
            'explanation': ctk.CTkEntry(self, placeholder_text="Penjelasan Soal", width=300)
        }

        for entry in self.entries.values():
            entry.pack(pady=5)

        self.status = ctk.CTkLabel(self, text="")
        self.status.pack(pady=5)

        ctk.CTkButton(self, text="Simpan Soal", command=self.simpan_soal).pack(pady=10)
        ctk.CTkButton(self, text="Lihat Laporan Nilai Siswa", command=self.view_reports).pack(pady=10)
        ctk.CTkButton(self, text="Keluar", command=lambda: exit_to_login(self)).pack(pady=10)

    def simpan_soal(self):
        data = [entry.get() for entry in self.entries.values()]
        if all(data):
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(""" 
                INSERT INTO questions 
                (question, option_a, option_b, option_c, option_d, correct_answer, explanation) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, tuple(data))
            conn.commit()
            conn.close()
            self.status.configure(text="Soal berhasil ditambahkan!", text_color="green")
        else:
            self.status.configure(text="Mohon isi semua data soal.", text_color="orange")

    def view_reports(self):
        # Menampilkan laporan nilai siswa
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, score FROM reports")
        reports = cursor.fetchall()
        conn.close()

        report_text = "\n".join([f"Siswa ID: {report[0]} - Skor: {report[1]}" for report in reports])
        self.status.configure(text=report_text, text_color="black")


# Halaman Siswa
class SiswaApp(ctk.CTk):
    def __init__(self, user_id):
        super().__init__()
        self.title("Siswa - Kerjakan Soal")
        self.geometry("400x500")
        self.user_id = user_id
        self.current_index = 0
        self.score = 0
        self.selected_answers = {}
        self.load_questions()

    def load_questions(self):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM questions")
        self.questions = cursor.fetchall()
        conn.close()

        if self.questions:
            self.show_question(self.current_index)
        else:
            ctk.CTkLabel(self, text="Belum ada soal.").pack(pady=10)
            ctk.CTkButton(self, text="Keluar", command=lambda: exit_to_login(self)).pack(pady=10)

    def show_question(self, index):
        for widget in self.winfo_children():
            widget.destroy()

        self.current_q = self.questions[index]
        ctk.CTkLabel(self, text=f"({index + 1}) {self.current_q[1]}").pack(pady=10)

        self.answer_status = ctk.CTkLabel(self, text="")
        self.answer_status.pack(pady=5)

        options = [self.current_q[2], self.current_q[3], self.current_q[4], self.current_q[5]]
        for opt in options:
            ctk.CTkButton(self, text=opt, command=lambda o=opt: self.handle_answer(o)).pack(pady=3)

        if index < len(self.questions) - 1:
            ctk.CTkButton(self, text="Next", command=lambda: self.show_question(index + 1)).pack(pady=10)
        else:
            ctk.CTkButton(self, text="Submit", command=self.finalize_quiz).pack(pady=10)

    def handle_answer(self, option):
        self.selected_answers[self.current_q[0]] = option
        if option == self.current_q[6]:  # correct_answer
            self.score += 1
            self.answer_status.configure(text="Jawaban benar!", text_color="green")
        else:
            self.answer_status.configure(
                text=f"Salah. Penjelasan: {self.current_q[7]}", text_color="red"
            )

    def finalize_quiz(self):
        for widget in self.winfo_children():
            widget.destroy()

        total = len(self.questions)
        nilai = int((self.score / total) * 100)

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO reports (user_id, score) VALUES (?, ?)", (self.user_id, nilai))
        conn.commit()
        conn.close()

        ctk.CTkLabel(self, text=f"Skor Anda: {nilai}").pack(pady=20)
        ctk.CTkLabel(self, text="Soal berhasil disubmit. Terima kasih!").pack(pady=5)
        ctk.CTkButton(self, text="Keluar", command=lambda: exit_to_login(self)).pack(pady=10)


# Halaman Registrasi
class RegisterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Halaman Registrasi")
        self.geometry("300x350")
        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self, text="Daftar Akun Baru").pack(pady=10)

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Nama Pengguna")
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Kata Sandi", show="*")
        self.password_entry.pack(pady=10)

        ctk.CTkLabel(self, text="Pilih Peran:").pack(pady=5)
        self.role_option = ctk.CTkOptionMenu(self, values=["siswa", "guru"])
        self.role_option.set("siswa")
        self.role_option.pack(pady=5)

        ctk.CTkButton(self, text="Daftar", command=self.register).pack(pady=20)
        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.pack()

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_option.get()

        if username and password and role:
            success = register_user(username, password, role)
            if success:
                self.status_label.configure(text="Registrasi berhasil!", text_color="green")
            else:
                self.status_label.configure(text="Username sudah digunakan!", text_color="red")
        else:
            self.status_label.configure(text="Isi semua data!", text_color="orange")


if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
