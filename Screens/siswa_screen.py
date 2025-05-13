import customtkinter as ctk
from db import connect_db
from screeninfo import get_monitors



class SiswaApp(ctk.CTk):
    def __init__(self, user_id, previous_screen=None):
        super().__init__()
        self.title("Siswa - Kerjakan Soal")
        self.set_fullscreen_windowed()
        self.user_id = user_id
        self.previous_screen = previous_screen  # Simpan referensi ke screen sebelumnya
        self.current_index = 0
        self.score = 0
        self.selected_answers = {}
        self.load_questions()

    def set_fullscreen_windowed(self):
        # Dapatkan resolusi layar utama
        monitor = get_monitors()[0]
        screen_width = monitor.width
        screen_height = monitor.height

        # Atur ukuran jendela agar sesuai dengan resolusi layar
        self.geometry(f"{screen_width}x{screen_height}+0+0")

    def load_questions(self):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM questions")
        self.questions = cursor.fetchall()
        conn.close()

        if self.questions:
            self.show_question(self.current_index)
        else:
            ctk.CTkLabel(self, text="Belum ada soal.", font=("Arial", 16)).place(relx=0.5, rely=0.4, anchor="center")
            ctk.CTkButton(self, text="Keluar", command=self.exit_to_login).place(relx=0.5, rely=0.6, relwidth=0.2, relheight=0.07, anchor="center")

    def show_question(self, index):
        for widget in self.winfo_children():
            widget.destroy()

        self.current_q = self.questions[index]
        ctk.CTkLabel(self, text=f"({index + 1}) {self.current_q[1]}", font=("Arial", 16)).place(relx=0.5, rely=0.1, anchor="center")

        self.answer_status = ctk.CTkLabel(self, text="", font=("Arial", 14))
        self.answer_status.place(relx=0.5, rely=0.8, anchor="center")

        options = [self.current_q[2], self.current_q[3], self.current_q[4], self.current_q[5]]
        for i, opt in enumerate(options):
            ctk.CTkButton(self, text=opt, command=lambda o=opt: self.handle_answer(o)).place(
                relx=0.5, rely=0.2 + i * 0.1, relwidth=0.6, relheight=0.07, anchor="center"
            )

        if index < len(self.questions) - 1:
            ctk.CTkButton(self, text="Next", command=lambda: self.show_question(index + 1)).place(
                relx=0.4, rely=0.9, relwidth=0.2, relheight=0.07
            )
        else:
            ctk.CTkButton(self, text="Submit", command=self.finalize_quiz).place(
                relx=0.6, rely=0.9, relwidth=0.2, relheight=0.07
            )

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

        ctk.CTkLabel(self, text=f"Skor Anda: {nilai}", font=("Arial", 16)).place(relx=0.5, rely=0.4, anchor="center")
        ctk.CTkLabel(self, text="Soal berhasil disubmit. Terima kasih!", font=("Arial", 14)).place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkButton(self, text="Keluar", command=self.exit_to_login).place(relx=0.5, rely=0.6, relwidth=0.2, relheight=0.07, anchor="center")

    def exit_to_login(self):
        from Screens.login_screen import LoginApp
        self.destroy()
        login_app = LoginApp()
        login_app.mainloop()

    def back_to_previous(self):
        self.destroy()
        if self.previous_screen:
            self.previous_screen.deiconify()  # Tampilkan kembali screen sebelumnya