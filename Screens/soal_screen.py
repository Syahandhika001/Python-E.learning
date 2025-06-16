import customtkinter as ctk
from db import connect_db
from screeninfo import get_monitors

class SoalScreen(ctk.CTk):
    def __init__(self, user_id, previous_screen=None):
        super().__init__()
        self.title("SoalScreen")
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
        ctk.CTkLabel(self, text="Daftar Soal", font=("Arial", 24)).place(relx=0.5, rely=0.05, anchor="center")
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.place(relx=0.5, rely=0.4, relwidth=0.8, relheight=0.5, anchor="center")
        self.load_soal()

        # Pilih materi
        ctk.CTkLabel(self, text="Pilih Materi:").place(relx=0.2, rely=0.8, anchor="w")
        self.materi_option = ctk.CTkOptionMenu(self, values=self.get_materi_list())
        self.materi_option.place(relx=0.3, rely=0.8, anchor="w")
        ctk.CTkLabel(self, text="Soal:").place(relx=0.2, rely=0.85, anchor="w")
        self.soal_entry = ctk.CTkEntry(self, width=300)
        self.soal_entry.place(relx=0.3, rely=0.85, anchor="w")
        ctk.CTkLabel(self, text="A:").place(relx=0.2, rely=0.88, anchor="w")
        self.a_entry = ctk.CTkEntry(self, width=100)
        self.a_entry.place(relx=0.23, rely=0.88, anchor="w")
        ctk.CTkLabel(self, text="B:").place(relx=0.35, rely=0.88, anchor="w")
        self.b_entry = ctk.CTkEntry(self, width=100)
        self.b_entry.place(relx=0.38, rely=0.88, anchor="w")
        ctk.CTkLabel(self, text="C:").place(relx=0.5, rely=0.88, anchor="w")
        self.c_entry = ctk.CTkEntry(self, width=100)
        self.c_entry.place(relx=0.53, rely=0.88, anchor="w")
        ctk.CTkLabel(self, text="D:").place(relx=0.65, rely=0.88, anchor="w")
        self.d_entry = ctk.CTkEntry(self, width=100)
        self.d_entry.place(relx=0.68, rely=0.88, anchor="w")
        ctk.CTkLabel(self, text="Jawaban Benar:").place(relx=0.2, rely=0.91, anchor="w")
        self.correct_entry = ctk.CTkEntry(self, width=100)
        self.correct_entry.place(relx=0.3, rely=0.91, anchor="w")
        ctk.CTkLabel(self, text="Penjelasan:").place(relx=0.45, rely=0.91, anchor="w")
        self.explanation_entry = ctk.CTkEntry(self, width=200)
        self.explanation_entry.place(relx=0.55, rely=0.91, anchor="w")
        self.status_label = ctk.CTkLabel(self, text="", font=("Arial", 12))
        self.status_label.place(relx=0.5, rely=0.96, anchor="center")
        ctk.CTkButton(self, text="Tambah/Update Soal", command=self.save_soal).place(relx=0.8, rely=0.85, relwidth=0.15, relheight=0.07)
        ctk.CTkButton(self, text="Hapus Soal", command=self.delete_soal).place(relx=0.8, rely=0.92, relwidth=0.15, relheight=0.07)
        ctk.CTkButton(self, text="Kembali", command=self.back_to_dashboard).place(relx=0.9, rely=0.97, relwidth=0.08, relheight=0.05)
        self.selected_id = None

    def get_materi_list(self):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, judul FROM materi")
        rows = cursor.fetchall()
        conn.close()
        return [f"{id_materi} - {judul}" for id_materi, judul in rows] if rows else ["-"]

    def load_soal(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT questions.id, materi.judul, questions.question FROM questions JOIN materi ON questions.materi_id = materi.id")
        rows = cursor.fetchall()
        conn.close()
        ctk.CTkLabel(self.table_frame, text="Materi", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=10, pady=5)
        ctk.CTkLabel(self.table_frame, text="Soal", font=("Arial", 14, "bold")).grid(row=0, column=1, padx=10, pady=5)
        for i, (id_soal, judul, soal) in enumerate(rows, start=1):
            btn = ctk.CTkButton(self.table_frame, text=soal, command=lambda i=id_soal: self.select_soal(i), anchor="w")
            btn.grid(row=i, column=1, sticky="w", padx=10, pady=5)
            ctk.CTkLabel(self.table_frame, text=judul, anchor="w").grid(row=i, column=0, sticky="w", padx=10, pady=5)

    def select_soal(self, id_soal):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM questions WHERE id=?", (id_soal,))
        soal = cursor.fetchone()
        conn.close()
        if soal and len(soal) >= 9:
            self.selected_id = soal[0]
            # urutan: id, question, a, b, c, d, correct, explanation, materi_id
            self.soal_entry.delete(0, 'end')
            self.soal_entry.insert(0, soal[1])
            self.a_entry.delete(0, 'end')
            self.a_entry.insert(0, soal[2])
            self.b_entry.delete(0, 'end')
            self.b_entry.insert(0, soal[3])
            self.c_entry.delete(0, 'end')
            self.c_entry.insert(0, soal[4])
            self.d_entry.delete(0, 'end')
            self.d_entry.insert(0, soal[5])
            self.correct_entry.delete(0, 'end')
            self.correct_entry.insert(0, soal[6])
            self.explanation_entry.delete(0, 'end')
            self.explanation_entry.insert(0, soal[7])
            materi_id = soal[8]
            for val in self.materi_option.cget('values'):
                if str(materi_id) == val.split(' - ')[0]:
                    self.materi_option.set(val)
                    break
            self.status_label.configure(text=f"Edit Soal ID: {id_soal}", text_color="orange")
        else:
            self.status_label.configure(text="Data soal tidak valid/tidak lengkap!", text_color="red")

    def save_soal(self):
        soal = self.soal_entry.get()
        a = self.a_entry.get()
        b = self.b_entry.get()
        c = self.c_entry.get()
        d = self.d_entry.get()
        correct = self.correct_entry.get()
        explanation = self.explanation_entry.get()
        materi_val = self.materi_option.get()
        if not soal or soal.strip().isdigit() or not a or not b or not c or not d or not correct or not materi_val or materi_val == "-":
            self.status_label.configure(text="Semua field wajib diisi dan field soal harus berupa pertanyaan!", text_color="red")
            return
        materi_id = int(materi_val.split(' - ')[0])
        print(f"DEBUG SIMPAN: materi_id={materi_id}, soal={soal}, a={a}, b={b}, c={c}, d={d}, correct={correct}, explanation={explanation}, selected_id={self.selected_id}")
        conn = connect_db()
        cursor = conn.cursor()
        if self.selected_id:
            cursor.execute("UPDATE questions SET question=?, option_a=?, option_b=?, option_c=?, option_d=?, correct_answer=?, explanation=?, materi_id=? WHERE id=?", (soal, a, b, c, d, correct, explanation, materi_id, self.selected_id))
            self.status_label.configure(text="Soal diperbarui!", text_color="green")
        else:
            cursor.execute("INSERT INTO questions (question, option_a, option_b, option_c, option_d, correct_answer, explanation, materi_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (soal, a, b, c, d, correct, explanation, materi_id))
            self.status_label.configure(text="Soal ditambahkan!", text_color="green")
        conn.commit()
        conn.close()
        self.selected_id = None
        self.soal_entry.delete(0, 'end')
        self.a_entry.delete(0, 'end')
        self.b_entry.delete(0, 'end')
        self.c_entry.delete(0, 'end')
        self.d_entry.delete(0, 'end')
        self.correct_entry.delete(0, 'end')
        self.explanation_entry.delete(0, 'end')
        self.load_soal()
        self.materi_option.configure(values=self.get_materi_list())

    def delete_soal(self):
        if not self.selected_id:
            self.status_label.configure(text="Pilih soal yang akan dihapus!", text_color="red")
            return
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM questions WHERE id=?", (self.selected_id,))
        conn.commit()
        conn.close()
        self.status_label.configure(text="Soal dihapus!", text_color="green")
        self.selected_id = None
        self.soal_entry.delete(0, 'end')
        self.a_entry.delete(0, 'end')
        self.b_entry.delete(0, 'end')
        self.c_entry.delete(0, 'end')
        self.d_entry.delete(0, 'end')
        self.correct_entry.delete(0, 'end')
        self.explanation_entry.delete(0, 'end')
        self.load_soal()
        self.materi_option.configure(values=self.get_materi_list())

    def back_to_dashboard(self):
        self.destroy()
        if self.previous_screen:
            self.previous_screen.deiconify()
