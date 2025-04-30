import customtkinter as ctk
from db import init_db, connect_db

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    
    def __init__(self):
        super().__init__()
        self.title("E-Learning Desktop App")
        self.geometry("900x600")

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=10)

        self.login_btn = ctk.CTkButton(self, text="login", command=self.login)
        self.login_btn.pack(pady=10)

        self.register_btn = ctk.CTkButton(self, text="Register", command=self.open_register_window)
        self.register_btn.pack(pady=5)


        self.output_label = ctk.CTkLabel(self, text="")
        self.output_label.pack(pady=10)
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username,password))
        user = cursor.fetchone()
        conn.close()

        if user:
            role = user[3]
            self.output_label.configure(text=f"Login berhasil sebagai {role}")
            self.show_question()
        else:
            self.output_label.configure(text="Login Gagal.")
    
    def show_question(self):
        for widget in self.winfo_children():
            widget.destroy()

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM question LIMIT 1")
        question = cursor.fetchone()
        conn.close()

        if question:
            q_label = ctk.CTkLabel(self, text=f"soal: {question[1]}")
            q_label.pack(pady=10)
        else:
            q_label = ctk.CTkLabel(self, text="Belum ada soal.")
            q_label.pack(pady=10)
    
    def open_register_window(self):
        register_window = ctk.CTkToplevel(self)
        register_window.title("Registrasi")
        register_window.geometry("300x300")

        username_entry = ctk.CTkEntry(register_window, placeholder_text="Username")
        username_entry.pack(pady=10)

        password_entry = ctk.CTkEntry(register_window, placeholder_text="Password", show="*")
        password_entry.pack(pady=10)

        role_option = ctk.CTkOptionMenu(register_window, values=["siswa", "guru"])
        role_option.set("siswa")  # default
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

    def open_dashboard(self, role):
        for widget in self.winfo_children():
            widget.destroy()

        if role == "guru":
            self.show_guru_view()
        elif role == "siswa":
            self.show_siswa_view()

    def show_guru_view(self):
        label = ctk.CTkLabel(self, text="Input Soal Baru (Guru)")
        label.pack(pady=10)

        question_entry = ctk.CTkEntry(self, placeholder_text="Tulis soal di sini", width=300)
        question_entry.pack(pady=10)

        answer_entry = ctk.CTkEntry(self, placeholder_text="Jawaban benar", width=300)
        answer_entry.pack(pady=10)

        def simpan_soal():
            question = question_entry.get()
            answer = answer_entry.get()

            if question and answer:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO questions (question, answer) VALUES (?, ?)", (question, answer))
                conn.commit()
                conn.close()
                label.configure(text="Soal berhasil ditambahkan!")
            else:
                label.configure(text="Mohon isi soal dan jawaban.")

        submit_btn = ctk.CTkButton(self, text="Simpan Soal", command=simpan_soal)
        submit_btn.pack(pady=10)

    def show_siswa_view(self):
        label = ctk.CTkLabel(self, text="Soal yang tersedia:")
        label.pack(pady=10)

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT question FROM questions")
        questions = cursor.fetchall()
        conn.close()

        if questions:
            for q in questions:
                q_label = ctk.CTkLabel(self, text=f"- {q[0]}")
                q_label.pack(anchor="w", padx=20)
        else:
            q_label = ctk.CTkLabel(self, text="Belum ada soal.")
            q_label.pack(pady=10)


if __name__ == "__main__":
    init_db()
    app = App()
    app.mainloop()