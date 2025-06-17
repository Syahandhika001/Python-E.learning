import customtkinter as ctk
from db import connect_db
from screeninfo import get_monitors



class GradientFrame(ctk.CTkFrame):
    def __init__(self, master, color1, color2, **kwargs):
        super().__init__(master, **kwargs)
        self.color1 = color1
        self.color2 = color2
        self.canvas = ctk.CTkCanvas(self, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.bind("<Configure>", self._draw_gradient)

    def _draw_gradient(self, event=None):
        self.canvas.delete("all")
        width = self.winfo_width()
        height = self.winfo_height()
        limit = height
        (r1, g1, b1) = self.winfo_rgb(self.color1)
        (r2, g2, b2) = self.winfo_rgb(self.color2)
        r_ratio = float(r2 - r1) / limit
        g_ratio = float(g2 - g1) / limit
        b_ratio = float(b2 - b1) / limit
        for i in range(limit):
            nr = int(r1 + (r_ratio * i))
            ng = int(g1 + (g_ratio * i))
            nb = int(b1 + (b_ratio * i))
            color = f'#{nr//256:02x}{ng//256:02x}{nb//256:02x}'
            self.canvas.create_line(0, i, width, i, fill=color)

class EditSoal(ctk.CTk):
    def __init__(self, soal_id, user_id, previous_screen=None):
        super().__init__()
        self.title("EditSoal")
        self.set_fullscreen_windowed()
        self.soal_id = soal_id
        self.user_id = user_id
        self.previous_screen = previous_screen  # Simpan referensi ke screen sebelumnya
        # Gradient background
        self.gradient = GradientFrame(self, "#ff6600", "#b34700")
        self.gradient.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.create_widgets()

    def set_fullscreen_windowed(self):
        # Dapatkan resolusi layar utama
        monitor = get_monitors()[0]
        screen_width = monitor.width
        screen_height = monitor.height

        # Atur ukuran jendela agar sesuai dengan resolusi layar
        self.geometry(f"{screen_width}x{screen_height}+0+0")

    def create_widgets(self):
        card = ctk.CTkFrame(self.gradient, fg_color="#f2f2f2", corner_radius=16)
        card.place(relx=0.5, rely=0.5, relwidth=0.7, relheight=0.8, anchor="center")
        ctk.CTkLabel(card, text="Edit Soal", font=("Arial", 28, "bold"), text_color="#ff6600").place(relx=0.5, rely=0.08, anchor="center")

        # Ambil data soal dari database
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM questions WHERE id=?", (self.soal_id,))
        soal = cursor.fetchone()
        conn.close()

        # Entry fields untuk mengedit soal
        self.entries = {
            'question': ctk.CTkEntry(card, placeholder_text="Tulis soal di sini", fg_color="#fff7e6"),
            'a': ctk.CTkEntry(card, placeholder_text="Pilihan A", fg_color="#fff7e6"),
            'b': ctk.CTkEntry(card, placeholder_text="Pilihan B", fg_color="#fff7e6"),
            'c': ctk.CTkEntry(card, placeholder_text="Pilihan C", fg_color="#fff7e6"),
            'd': ctk.CTkEntry(card, placeholder_text="Pilihan D", fg_color="#fff7e6"),
            'correct': ctk.CTkEntry(card, placeholder_text="Jawaban Benar", fg_color="#fff7e6"),
            'explanation': ctk.CTkEntry(card, placeholder_text="Penjelasan Soal", fg_color="#fff7e6")
        }

        # Isi entry fields dengan data soal
        if soal:
            keys = ['question', 'a', 'b', 'c', 'd', 'correct', 'explanation']
            for i, key in enumerate(keys):
                self.entries[key].insert(0, soal[i + 1])  # Data mulai dari kolom kedua
                self.entries[key].place(relx=0.5, rely=0.22 + i * 0.09, relwidth=0.6, relheight=0.06, anchor="center")

        # Tombol Simpan Perubahan
        ctk.CTkButton(card, text="Simpan Perubahan", command=self.update_soal, fg_color="#ff6600", hover_color="#b34700", text_color="white", font=("Arial", 16, "bold")).place(relx=0.4, rely=0.85, relwidth=0.18, relheight=0.08)

        # Tombol Kembali
        ctk.CTkButton(card, text="Kembali", command=self.back_to_previous, fg_color="#b34700", hover_color="#ff6600", text_color="white", font=("Arial", 16, "bold")).place(relx=0.6, rely=0.85, relwidth=0.18, relheight=0.08)


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