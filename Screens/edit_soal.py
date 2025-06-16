import customtkinter as ctk
from db import connect_db
from screeninfo import get_monitors



class EditSoal(ctk.CTk):
    def __init__(self, soal_id, user_id, previous_screen=None):
        super().__init__()
        self.title("EditSoal")
        self.set_fullscreen_windowed()
        self.soal_id = soal_id
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
        ctk.CTkLabel(self, text="Edit Soal", font=("Arial", 24)).place(relx=0.5, rely=0.05, anchor="center")

        # Ambil data soal dari database
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM questions WHERE id=?", (self.soal_id,))
        soal = cursor.fetchone()
        conn.close()

        # Entry fields untuk mengedit soal
        self.entries = {
            'question': ctk.CTkEntry(self, placeholder_text="Tulis soal di sini"),
            'a': ctk.CTkEntry(self, placeholder_text="Pilihan A"),
            'b': ctk.CTkEntry(self, placeholder_text="Pilihan B"),
            'c': ctk.CTkEntry(self, placeholder_text="Pilihan C"),
            'd': ctk.CTkEntry(self, placeholder_text="Pilihan D"),
            'correct': ctk.CTkEntry(self, placeholder_text="Jawaban Benar"),
            'explanation': ctk.CTkEntry(self, placeholder_text="Penjelasan Soal")
        }

        # Isi entry fields dengan data soal
        if soal:
            keys = ['question', 'a', 'b', 'c', 'd', 'correct', 'explanation']
            for i, key in enumerate(keys):
                self.entries[key].insert(0, soal[i + 1])  # Data mulai dari kolom kedua
                self.entries[key].place(relx=0.5, rely=0.15 + i * 0.1, relwidth=0.6, relheight=0.05, anchor="center")

        # Tombol Simpan Perubahan
        ctk.CTkButton(self, text="Simpan Perubahan", command=self.update_soal).place(
            relx=0.4, rely=0.85, relwidth=0.2, relheight=0.07
        )

        # Tombol Kembali
        ctk.CTkButton(self, text="Kembali", command=self.back_to_previous).place(
            relx=0.6, rely=0.85, relwidth=0.2, relheight=0.07
        )


    def update_soal(self):
        # Ambil data dari entry fields
        data = [entry.get() for entry in self.entries.values()]
        if all(data):
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE questions
                SET question=?, option_a=?, option_b=?, option_c=?, option_d=?, correct_answer=?, explanation=?
                WHERE id=?
            """, (*data, self.soal_id))
            conn.commit()
            conn.close()
            ctk.CTkLabel(self, text="Soal berhasil diperbarui!", text_color="green").place(relx=0.5, rely=0.9, anchor="center")
        else:
            ctk.CTkLabel(self, text="Mohon isi semua data soal.", text_color="red").place(relx=0.5, rely=0.9, anchor="center")
    
    def back_to_previous(self):
        self.destroy()
        if self.previous_screen:
            self.previous_screen.deiconify()   # Tampilkan kembali screen sebelumnya