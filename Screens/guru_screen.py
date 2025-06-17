import customtkinter as ctk
from db import connect_db
from Screens.login_screen import LoginApp
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


class GuruApp(ctk.CTk):
    def __init__(self, user_id, previous_screen=None):
        super().__init__()
        self.title("Input Soal - Guru")
        self.set_fullscreen_windowed()
        self.user_id = user_id
        self.previous_screen = previous_screen

        self.ensure_column_materi_id_exists()

        # Gradient background
        self.gradient = GradientFrame(self, "#ff6600", "#b34700")
        self.gradient.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.create_widgets()

    def set_fullscreen_windowed(self):
        monitor = get_monitors()[0]
        self.geometry(f"{monitor.width}x{monitor.height}+0+0")

    def create_widgets(self):
        card = ctk.CTkFrame(self.gradient, fg_color="#f2f2f2", corner_radius=16)
        card.place(relx=0.5, rely=0.5, relwidth=0.7, relheight=0.8, anchor="center")

        ctk.CTkLabel(card, text="Input Soal Pilihan Ganda", font=("Arial", 28, "bold"), text_color="#ff6600").place(relx=0.5, rely=0.08, anchor="center")
        ctk.CTkLabel(card, text="Pilih Materi:", font=("Arial", 14, "bold"), text_color="#b34700").place(relx=0.2, rely=0.16, anchor="w")

        self.materi_option = ctk.CTkOptionMenu(card, values=self.get_materi_list(), fg_color="#ff6600", text_color="white")
        self.materi_option.place(relx=0.3, rely=0.16, anchor="w")

        # Input fields
        self.entries = {
            'question': ctk.CTkEntry(card, placeholder_text="Tulis soal di sini, contoh: 1 + 1 = ...?", fg_color="#fff7e6"),
            'a': ctk.CTkEntry(card, placeholder_text="Pilihan A", fg_color="#fff7e6"),
            'b': ctk.CTkEntry(card, placeholder_text="Pilihan B", fg_color="#fff7e6"),
            'c': ctk.CTkEntry(card, placeholder_text="Pilihan C", fg_color="#fff7e6"),
            'd': ctk.CTkEntry(card, placeholder_text="Pilihan D", fg_color="#fff7e6"),
            'correct': ctk.CTkEntry(card, placeholder_text="Jawaban Benar (misal: A)", fg_color="#fff7e6"),
            'explanation': ctk.CTkEntry(card, placeholder_text="Penjelasan Soal", fg_color="#fff7e6")
        }

        for i, entry in enumerate(self.entries.values()):
            entry.place(relx=0.5, rely=0.25 + i * 0.08, relwidth=0.6, relheight=0.06, anchor="center")

        self.status = ctk.CTkLabel(card, text="", font=("Arial", 14))
        self.status.place(relx=0.5, rely=0.75, anchor="center")

        ctk.CTkButton(card, text="Simpan Soal", command=self.simpan_soal, fg_color="#ff6600", hover_color="#b34700", text_color="white", font=("Arial", 16, "bold")).place(relx=0.36, rely=0.85, relwidth=0.18, relheight=0.08)
        ctk.CTkButton(card, text="Dashboard Soal", command=self.open_dashboard_soal, fg_color="#f39c12", hover_color="#e67e22", text_color="white", font=("Arial", 16, "bold")).place(relx=0.56, rely=0.85, relwidth=0.18, relheight=0.08)
        ctk.CTkButton(card, text="Kembali", command=self.back_to_previous, fg_color="#b34700", hover_color="#ff6600", text_color="white", font=("Arial", 16, "bold")).place(relx=0.76, rely=0.85, relwidth=0.18, relheight=0.08)

    def ensure_column_materi_id_exists(self):
        try:
            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("PRAGMA table_info(questions)")
            columns = [col[1] for col in cursor.fetchall()]

            if "materi_id" not in columns:
                cursor.execute("ALTER TABLE questions ADD COLUMN materi_id INTEGER")
                conn.commit()

            conn.close()
        except Exception as e:
            print("Gagal memastikan kolom materi_id:", e)

    def get_materi_list(self):
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT id, judul FROM materi")
            rows = cursor.fetchall()
            conn.close()
            return [f"{id} - {judul}" for id, judul in rows] if rows else ["-"]
        except Exception as e:
            print("Gagal memuat materi:", e)
            return ["-"]

    def simpan_soal(self):
        materi_val = self.materi_option.get()
        if not materi_val or materi_val == "-":
            self.status.configure(text="Pilih materi terlebih dahulu!", text_color="red")
            return

        try:
            materi_id = int(materi_val.split(" - ")[0])
        except:
            self.status.configure(text="Format materi tidak valid!", text_color="red")
            return

        data = {key: entry.get().strip() for key, entry in self.entries.items()}

        if not data['question'] or data['question'].isdigit():
            self.status.configure(text="Soal harus berupa teks pertanyaan!", text_color="red")
            return

        if not all(data.values()):
            self.status.configure(text="Semua field harus diisi!", text_color="orange")
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO questions (materi_id, question, option_a, option_b, option_c, option_d, correct_answer, explanation)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                materi_id,
                data['question'], data['a'], data['b'], data['c'], data['d'],
                data['correct'].upper(),
                data['explanation']
            ))
            conn.commit()
            conn.close()

            self.status.configure(text="Soal berhasil disimpan!", text_color="green")
            for entry in self.entries.values():
                entry.delete(0, "end")

        except Exception as e:
            print("Gagal simpan soal:", e)
            self.status.configure(text="Terjadi kesalahan saat menyimpan!", text_color="red")

    def open_dashboard_soal(self):
        from Screens.semua_soal_screen import SemuaSoalScreen
        self.destroy()
        SemuaSoalScreen(self.user_id, previous_screen=self.previous_screen).mainloop()

    def back_to_previous(self):
        self.destroy()
        if self.previous_screen:
            self.previous_screen.deiconify()

    def exit_to_login(self):
        self.destroy()
        LoginApp().mainloop()
