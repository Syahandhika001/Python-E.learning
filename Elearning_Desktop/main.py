import customtkinter as ctk
from db import init_db, connect_db
from customtkinter import CTkToplevel

# Inisialisasi database
init_db()

# Pengaturan tampilan
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("E-Learning Desktop App")
        self.geometry("900x600")

        # Entry untuk Username dan Password
        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=10)

        # Tombol Login
        self.login_btn = ctk.CTkButton(self, text="Login", command=self.login)
        self.login_btn.pack(pady=10)

        # Tombol Register
        self.register_btn = ctk.CTkButton(self, text="Register", command=self.open_register_window)
        self.register_btn.pack(pady=5)

        # Label untuk output
        self.output_label = ctk.CTkLabel(self, text="")
        self.output_label.pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            role = user[3]
            self.output_label.configure(text=f"Login berhasil sebagai {role}")
            self.open_dashboard(role, user[0])
        else:
            self.output_label.configure(text="Login Gagal.")

    def open_register_window(self):
        register_window = CTkToplevel(self)
        register_window.title("Registrasi")
        register_window.geometry("300x300")

        username_entry = ctk.CTkEntry(register_window, placeholder_text="Username")
        username_entry.pack(pady=10)

        password_entry = ctk.CTkEntry(register_window, placeholder_text="Password", show="*")
        password_entry.pack(pady=10)

        role_option = ctk.CTkOptionMenu(register_window, values=["siswa", "guru"])
        role_option.set("siswa")
        role_option.pack(pady=10)

        def submit_register():
            username = username_entry.get()
            password = password_entry.get()
            role = role_option.get()

            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
            conn.commit()
            conn.close()

            register_window.destroy()
            self.output_label.configure(text="Registrasi berhasil!")

        submit_btn = ctk.CTkButton(register_window, text="Submit", command=submit_register)
        submit_btn.pack(pady=10)

    def open_dashboard(self, role, user_id):
        for widget in self.winfo_children():
            widget.destroy()

        if role == "guru":
            self.show_guru_view(user_id)
        elif role == "siswa":
            self.show_siswa_view(user_id)

    def show_guru_view(self, user_id):
        label = ctk.CTkLabel(self, text="Input Soal Pilihan Ganda (Guru)")
        label.pack(pady=10)

        # Form input soal
        question_entry = ctk.CTkEntry(self, placeholder_text="Tulis soal di sini", width=300)
        question_entry.pack(pady=10)

        option_a_entry = ctk.CTkEntry(self, placeholder_text="Pilihan A", width=300)
        option_a_entry.pack(pady=5)

        option_b_entry = ctk.CTkEntry(self, placeholder_text="Pilihan B", width=300)
        option_b_entry.pack(pady=5)

        option_c_entry = ctk.CTkEntry(self, placeholder_text="Pilihan C", width=300)
        option_c_entry.pack(pady=5)

        option_d_entry = ctk.CTkEntry(self, placeholder_text="Pilihan D", width=300)
        option_d_entry.pack(pady=5)

        correct_answer_entry = ctk.CTkEntry(self, placeholder_text="Jawaban Benar", width=300)
        correct_answer_entry.pack(pady=5)

        def simpan_soal():
            question = question_entry.get()
            option_a = option_a_entry.get()
            option_b = option_b_entry.get()
            option_c = option_c_entry.get()
            option_d = option_d_entry.get()
            correct_answer = correct_answer_entry.get()

            if all([question, option_a, option_b, option_c, option_d, correct_answer]):
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO questions (question, option_a, option_b, option_c, option_d, correct_answer) VALUES (?, ?, ?, ?, ?, ?)",
                               (question, option_a, option_b, option_c, option_d, correct_answer))
                conn.commit()
                conn.close()
                label.configure(text="Soal berhasil ditambahkan!")
            else:
                label.configure(text="Mohon isi semua data soal.")

        submit_btn = ctk.CTkButton(self, text="Simpan Soal", command=simpan_soal)
        submit_btn.pack(pady=10)

        report_btn = ctk.CTkButton(self, text="Lihat Laporan Nilai Siswa", command=self.view_reports)
        report_btn.pack(pady=10)

        exit_btn = ctk.CTkButton(self, text="Keluar", command=self.exit_to_login)
        exit_btn.pack(pady=10)

    def view_reports(self):
        report_window = CTkToplevel(self)
        report_window.title("Laporan Nilai Siswa")
        report_window.geometry("600x400")

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''SELECT u.username, r.score
                          FROM reports r
                          JOIN users u ON r.user_id = u.id
                          WHERE u.role = 'siswa' ORDER BY r.score DESC''')
        reports = cursor.fetchall()
        conn.close()

        if reports:
            for report in reports:
                report_label = ctk.CTkLabel(report_window, text=f"Siswa: {report[0]} - Skor: {report[1]}")
                report_label.pack(pady=5)
        else:
            no_report_label = ctk.CTkLabel(report_window, text="Tidak ada laporan nilai siswa.")
            no_report_label.pack(pady=10)

    def show_siswa_view(self, user_id):
        label = ctk.CTkLabel(self, text="Soal yang tersedia:")
        label.pack(pady=10)

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM questions")
        questions = cursor.fetchall()
        conn.close()

        current_question_index = 0
        score = 0

        def load_next_question():
            nonlocal current_question_index
            if current_question_index < len(questions):
                q = questions[current_question_index]
                q_label.configure(text=f"- {q[1]}")

                option_a_btn.configure(text=f"A. {q[2]}", command=lambda: self.submit_answer(user_id, q[0], q[2], score))
                option_b_btn.configure(text=f"B. {q[3]}", command=lambda: self.submit_answer(user_id, q[0], q[3], score))
                option_c_btn.configure(text=f"C. {q[4]}", command=lambda: self.submit_answer(user_id, q[0], q[4], score))
                option_d_btn.configure(text=f"D. {q[5]}", command=lambda: self.submit_answer(user_id, q[0], q[5], score))
            else:
                self.show_final_score(score)

        if questions:
            q = questions[current_question_index]
            q_label = ctk.CTkLabel(self, text=f"- {q[1]}")
            q_label.pack(anchor="w", padx=20)

            option_a_btn = ctk.CTkButton(self, text=f"A. {q[2]}")
            option_a_btn.pack(pady=5)
            option_b_btn = ctk.CTkButton(self, text=f"B. {q[3]}")
            option_b_btn.pack(pady=5)
            option_c_btn = ctk.CTkButton(self, text=f"C. {q[4]}")
            option_c_btn.pack(pady=5)
            option_d_btn = ctk.CTkButton(self, text=f"D. {q[5]}")
            option_d_btn.pack(pady=5)

            next_btn = ctk.CTkButton(self, text="Next", command=load_next_question)
            next_btn.pack(pady=10)

            submit_btn = ctk.CTkButton(self, text="Submit", command=lambda: self.submit_final_score(user_id, score))
            submit_btn.pack(pady=10)
        else:
            q_label = ctk.CTkLabel(self, text="Belum ada soal.")
            q_label.pack(pady=10)

        exit_btn = ctk.CTkButton(self, text="Keluar", command=self.exit_to_login)
        exit_btn.pack(pady=10)

    def submit_answer(self, user_id, question_id, answer, score):
        conn = connect_db()
        cursor = conn.cursor()

        # Mengecek jawaban yang benar
        cursor.execute("SELECT correct_answer FROM questions WHERE id=?", (question_id,))
        correct = cursor.fetchone()[0]
        is_correct = (answer == correct)
        score = 100 if is_correct else 0

        # Menyimpan laporan nilai siswa
        cursor.execute("INSERT INTO reports (user_id, question_id, score) VALUES (?, ?, ?)", (user_id, question_id, score))
        conn.commit()
        conn.close()

        self.output_label.configure(text="Jawaban berhasil dikirim!")

    def submit_final_score(self, user_id, score):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO reports (user_id, score) VALUES (?, ?)", (user_id, score))
        conn.commit()
        conn.close()

        self.output_label.configure(text=f"Skor Anda: {score}")

    def exit_to_login(self):
        self.destroy()
        app = App()
        app.mainloop()

# Entry point aplikasi
if __name__ == "__main__":
    app = App()
    app.mainloop()
