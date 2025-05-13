import customtkinter as ctk
from db import connect_db
from Screens.login_screen import LoginApp
from screeninfo import get_monitors


class GuruApp(ctk.CTk):
    def __init__(self, user_id, previous_screen=None):
        super().__init__()
        self.title("Guru - Input Soal")
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
            'question': ctk.CTkEntry(self, placeholder_text="Tulis soal di sini"),
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

        # Status label
        self.status = ctk.CTkLabel(self, text="", font=("Arial", 14))
        self.status.place(relx=0.5, rely=0.85, anchor="center")

        # Tombol Simpan Soal
        save_button = ctk.CTkButton(self, text="Simpan Soal", command=self.simpan_soal)
        save_button.place(relx=0.4, rely=0.75, relwidth=0.2, relheight=0.07)

        # Tombol Kembali
        exit_button = ctk.CTkButton(self, text="Kembali", command=self.back_to_previous)
        exit_button.place(relx=0.6, rely=0.75, relwidth=0.2, relheight=0.07)

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

    def exit_to_login(self):
        self.destroy()
        login_app = LoginApp()
        login_app.mainloop()

    def back_to_previous(self):
        self.destroy()
        if self.previous_screen:
            self.previous_screen.deiconify()  # Tampilkan kembali screen sebelumnya