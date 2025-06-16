import customtkinter as ctk
from db import connect_db
from Screens.login_screen import LoginApp
from screeninfo import get_monitors


class GuruApp(ctk.CTk):
    def __init__(self, user_id, previous_screen=None):
        super().__init__()
        self.title("GuruScreen")
        self.set_fullscreen_windowed()
        self.user_id = user_id
        self.previous_screen = previous_screen  # Simpan referensi ke screen sebelumnya
        self.create_widgets()

    def set_fullscreen_windowed(self):
        # Dapatkan resolusi layar utama
        monitor = get_monitors()[0]
        screen_width = monitor.width
        screen_height = monitor.height

        # Atur ukuran jendela agar sesuai dengan resolusi layar
        self.geometry(f"{screen_width}x{screen_height}+0+0")

    def create_widgets(self):
        # Label judul
        title_label = ctk.CTkLabel(self, text="Input Soal Pilihan Ganda (Guru)", font=("Arial", 24))
        title_label.place(relx=0.5, rely=0.05, anchor="center")

        # Entry fields
        self.entries = {
            'question': ctk.CTkEntry(self, placeholder_text="Tulis soal di sini, misal: 1+1 = ...?"),
            'a': ctk.CTkEntry(self, placeholder_text="Pilihan A"),
            'b': ctk.CTkEntry(self, placeholder_text="Pilihan B"),
            'c': ctk.CTkEntry(self, placeholder_text="Pilihan C"),
            'd': ctk.CTkEntry(self, placeholder_text="Pilihan D"),
            'correct': ctk.CTkEntry(self, placeholder_text="Jawaban Benar"),
            'explanation': ctk.CTkEntry(self, placeholder_text="Penjelasan Soal")
        }

        # Tempatkan entry fields secara dinamis
        for i, (key, entry) in enumerate(self.entries.items()):
            entry.place(relx=0.5, rely=0.15 + i * 0.1, relwidth=0.6, relheight=0.05, anchor="center")

        # Pilihan materi
        ctk.CTkLabel(self, text="Pilih Materi:").place(relx=0.2, rely=0.12, anchor="w")
        self.materi_option = ctk.CTkOptionMenu(self, values=self.get_materi_list())
        self.materi_option.place(relx=0.3, rely=0.12, anchor="w")

        # Status label
        self.status = ctk.CTkLabel(self, text="", font=("Arial", 14))
        self.status.place(relx=0.5, rely=0.85, anchor="center")

        # Tombol Simpan Soal
        save_button = ctk.CTkButton(self, text="Simpan Soal", command=self.simpan_soal)
        save_button.place(relx=0.4, rely=0.75, relwidth=0.2, relheight=0.07)

        # Tombol Kembali
        exit_button = ctk.CTkButton(self, text="Kembali", command=self.back_to_previous)
        exit_button.place(relx=0.6, rely=0.75, relwidth=0.2, relheight=0.07)

    def get_materi_list(self):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, judul FROM materi")
        rows = cursor.fetchall()
        conn.close()
        return [f"{id_materi} - {judul}" for id_materi, judul in rows] if rows else ["-"]

    def simpan_soal(self):
        materi_val = self.materi_option.get()
        if not materi_val or materi_val == "-":
            self.status.configure(text="Pilih materi terlebih dahulu!", text_color="red")
            return
        materi_id = int(materi_val.split(' - ')[0])
        data = [entry.get() for entry in self.entries.values()]
        # Validasi: soal tidak boleh hanya angka atau kosong
        if not data[0] or data[0].strip().isdigit():
            self.status.configure(text="Field soal harus berupa pertanyaan, bukan angka!", text_color="red")
            return
        if all(data):
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO questions 
                (materi_id, question, option_a, option_b, option_c, option_d, correct_answer, explanation) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (materi_id, *data))
            conn.commit()
            conn.close()
            self.status.configure(text="Soal berhasil ditambahkan!", text_color="green")
        else:
            self.status.configure(text="Mohon isi semua data soal.", text_color="orange")

    def exit_to_login(self):
        self.destroy()
        login_app = LoginApp()
        login_app.mainloop()

    def back_to_previous(self):
        self.destroy()
        if self.previous_screen:
            self.previous_screen.deiconify()  # Tampilkan kembali screen sebelumnya