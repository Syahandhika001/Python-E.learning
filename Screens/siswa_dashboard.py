import customtkinter as ctk
from db import connect_db
from screeninfo import get_monitors

class SiswaDashboard(ctk.CTk):
    def __init__(self, user_id, previous_screen=None):
        super().__init__()
        self.title("SiswaDashboard")
        self.set_fullscreen_windowed()
        self.user_id = user_id
        self.previous_screen = previous_screen
        self.create_widgets()

    def set_fullscreen_windowed(self):
        monitor = get_monitors()[0]
        screen_width = monitor.width
        screen_height = monitor.height
        self.geometry(f"{screen_width}x{screen_height}+0+0")

    def create_widgets(self):
        ctk.CTkLabel(self, text="Pilih Materi", font=("Arial", 24)).place(relx=0.5, rely=0.1, anchor="center")
        self.materi_option = ctk.CTkOptionMenu(self, values=self.get_materi_list())
        self.materi_option.place(relx=0.5, rely=0.2, anchor="center")
        ctk.CTkButton(self, text="Belajar", command=self.belajar).place(relx=0.4, rely=0.3, relwidth=0.15, relheight=0.08)
        ctk.CTkButton(self, text="Kerjakan Soal", command=self.kerjakan_soal).place(relx=0.6, rely=0.3, relwidth=0.15, relheight=0.08)
        ctk.CTkButton(self, text="Kembali", command=self.back_to_previous).place(relx=0.9, rely=0.9, relwidth=0.08, relheight=0.06)

    def get_materi_list(self):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, judul FROM materi")
        rows = cursor.fetchall()
        conn.close()
        return [f"{id_materi} - {judul}" for id_materi, judul in rows] if rows else ["-"]

    def belajar(self):
        materi_val = self.materi_option.get()
        if materi_val == "-":
            return
        materi_id = int(materi_val.split(' - ')[0])
        self.withdraw()
        SiswaBahanAjar(self.user_id, materi_id, previous_screen=self).mainloop()

    def kerjakan_soal(self):
        materi_val = self.materi_option.get()
        if materi_val == "-":
            return
        materi_id = int(materi_val.split(' - ')[0])
        self.withdraw()
        SiswaKerjakanSoal(self.user_id, materi_id, previous_screen=self).mainloop()

    def back_to_previous(self):
        self.destroy()
        if self.previous_screen:
            self.previous_screen.deiconify()

class SiswaBahanAjar(ctk.CTk):
    def __init__(self, user_id, materi_id, previous_screen=None):
        super().__init__()
        self.title("SiswaBahanAjar")
        self.set_fullscreen_windowed()
        self.user_id = user_id
        self.materi_id = materi_id
        self.previous_screen = previous_screen
        self.create_widgets()

    def set_fullscreen_windowed(self):
        monitor = get_monitors()[0]
        screen_width = monitor.width
        screen_height = monitor.height
        self.geometry(f"{screen_width}x{screen_height}+0+0")

    def create_widgets(self):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT judul FROM materi WHERE id=?", (self.materi_id,))
        materi = cursor.fetchone()
        ctk.CTkLabel(self, text=f"Bahan Ajar: {materi[0] if materi else ''}", font=("Arial", 22)).place(relx=0.5, rely=0.1, anchor="center")
        cursor.execute("SELECT nama_bahan, file_path FROM bahan_ajar WHERE materi_id=?", (self.materi_id,))
        bahan_list = cursor.fetchall()
        conn.close()
        frame = ctk.CTkFrame(self)
        frame.place(relx=0.5, rely=0.5, relwidth=0.7, relheight=0.6, anchor="center")
        if bahan_list:
            for i, (nama, file_path) in enumerate(bahan_list):
                ctk.CTkLabel(frame, text=f"{i+1}. {nama}", font=("Arial", 16)).grid(row=i, column=0, sticky="w", padx=10, pady=5)
                ctk.CTkLabel(frame, text=file_path, font=("Arial", 14), text_color="blue").grid(row=i, column=1, sticky="w", padx=10, pady=5)
        else:
            ctk.CTkLabel(frame, text="Belum ada bahan ajar.", font=("Arial", 16)).pack(pady=20)
        ctk.CTkButton(self, text="Kembali", command=self.back_to_dashboard).place(relx=0.9, rely=0.9, relwidth=0.08, relheight=0.06)

    def back_to_dashboard(self):
        self.destroy()
        if self.previous_screen:
            self.previous_screen.deiconify()

class SiswaKerjakanSoal(ctk.CTk):
    def __init__(self, user_id, materi_id, previous_screen=None):
        super().__init__()
        self.title("SiswaKerjakanSoal")
        self.set_fullscreen_windowed()
        self.user_id = user_id
        self.materi_id = materi_id
        self.previous_screen = previous_screen
        self.current_index = 0
        self.score = 0
        self.selected_answers = {}
        self.load_questions()

    def set_fullscreen_windowed(self):
        monitor = get_monitors()[0]
        screen_width = monitor.width
        screen_height = monitor.height
        self.geometry(f"{screen_width}x{screen_height}+0+0")

    def load_questions(self):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM questions WHERE materi_id=?", (self.materi_id,))
        self.questions = cursor.fetchall()
        conn.close()
        if self.questions:
            self.show_question(self.current_index)
        else:
            ctk.CTkLabel(self, text="Belum ada soal.", font=("Arial", 16)).place(relx=0.5, rely=0.4, anchor="center")
            ctk.CTkButton(self, text="Kembali", command=self.back_to_dashboard).place(relx=0.5, rely=0.6, relwidth=0.2, relheight=0.07, anchor="center")

    def show_question(self, index):
        for widget in self.winfo_children():
            widget.destroy()
        self.current_q = self.questions[index]
        print(f"DEBUG SOAL SISWA: {self.current_q}")  # Debug print seluruh field soal
        ctk.CTkLabel(self, text=f"({index + 1}) {self.current_q[1]}", font=("Arial", 16)).place(relx=0.5, rely=0.1, anchor="center")
        self.answer_status = ctk.CTkLabel(self, text="", font=("Arial", 14))
        self.answer_status.place(relx=0.5, rely=0.8, anchor="center")
        options = [self.current_q[2], self.current_q[3], self.current_q[4], self.current_q[5]]  # option_a, b, c, d
        for i, opt in enumerate(options):
            ctk.CTkButton(self, text=opt, command=lambda o=opt: self.handle_answer(o), font=("Arial", 14)).place(
                relx=0.5, rely=0.2 + i * 0.1, relwidth=0.6, relheight=0.07, anchor="center"
            )

    def handle_answer(self, option):
        # Cegah double answer
        qid = self.current_q[0]
        if qid in self.selected_answers:
            return
        self.selected_answers[qid] = option
        if option == self.current_q[7]:  # correct_answer ada di index 7
            self.score += 1
        self.current_index += 1
        if self.current_index < len(self.questions):
            self.show_question(self.current_index)
        else:
            self.finalize_quiz()

    def finalize_quiz(self):
        for widget in self.winfo_children():
            widget.destroy()
        total = len(self.questions)
        # Hitung skor berdasarkan selected_answers
        benar = 0
        for q in self.questions:
            qid = q[0]
            if qid in self.selected_answers and self.selected_answers[qid] == q[7]:
                benar += 1
        nilai = int((benar / total) * 100) if total > 0 else 0
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO reports (user_id, score) VALUES (?, ?)", (self.user_id, nilai))
        conn.commit()
        conn.close()
        ctk.CTkLabel(self, text=f"Skor Anda: {nilai}", font=("Arial", 16)).place(relx=0.5, rely=0.4, anchor="center")
        ctk.CTkLabel(self, text="Soal berhasil disubmit. Terima kasih!", font=("Arial", 14)).place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkButton(self, text="Kembali", command=self.back_to_dashboard).place(relx=0.5, rely=0.6, relwidth=0.2, relheight=0.07, anchor="center")

    def back_to_dashboard(self):
        self.destroy()
        if self.previous_screen:
            self.previous_screen.deiconify()
