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

class SemuaSoalScreen(ctk.CTk):
    def __init__(self, user_id, previous_screen=None):
        super().__init__()
        self.title("Dashboard Semua Soal")
        self.set_fullscreen_windowed()
        self.user_id = user_id
        self.previous_screen = previous_screen
        # Gradient background
        self.gradient = GradientFrame(self, "#ff6600", "#b34700")
        self.gradient.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.create_widgets()

    def set_fullscreen_windowed(self):
        monitor = get_monitors()[0]
        screen_width = monitor.width
        screen_height = monitor.height
        self.geometry(f"{screen_width}x{screen_height}+0+0")

    def create_widgets(self):
        card = ctk.CTkFrame(self.gradient, fg_color="#f2f2f2", corner_radius=16)
        card.place(relx=0.5, rely=0.5, relwidth=0.9, relheight=0.85, anchor="center")
        ctk.CTkLabel(card, text="Daftar Semua Soal", font=("Arial", 28, "bold"), text_color="#ff6600").place(relx=0.5, rely=0.07, anchor="center")
        self.table_frame = ctk.CTkFrame(card, fg_color="#fff7e6", corner_radius=8)
        self.table_frame.place(relx=0.5, rely=0.5, relwidth=0.97, relheight=0.75, anchor="center")
        self.load_soal()
        ctk.CTkButton(card, text="Tambah Soal Baru", command=self.tambah_soal, fg_color="#ff6600", hover_color="#b34700", text_color="white", font=("Arial", 16, "bold")).place(relx=0.18, rely=0.92, relwidth=0.18, relheight=0.07)
        ctk.CTkButton(card, text="Kembali", command=self.back_to_previous, fg_color="#b34700", hover_color="#ff6600", text_color="white", font=("Arial", 16, "bold")).place(relx=0.82, rely=0.92, relwidth=0.18, relheight=0.07)

    def load_soal(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, judul FROM materi")
        materi_list = cursor.fetchall()
        cursor.execute("SELECT id, materi_id, question, option_a, option_b, option_c, option_d, correct_answer, explanation FROM questions")
        soal_list = cursor.fetchall()
        conn.close()
        row_idx = 0
        for id_materi, judul_materi in materi_list:
            ctk.CTkLabel(self.table_frame, text=f"{judul_materi}", font=("Arial", 18, "bold"), text_color="#ff6600").grid(row=row_idx, column=0, padx=10, pady=(18,5), sticky="w", columnspan=8)
            row_idx += 1
            ctk.CTkLabel(self.table_frame, text="Soal", font=("Arial", 14, "bold"), text_color="#222222").grid(row=row_idx, column=0, padx=10, pady=5)
            ctk.CTkLabel(self.table_frame, text="A", font=("Arial", 14, "bold"), text_color="#222222").grid(row=row_idx, column=1, padx=10, pady=5)
            ctk.CTkLabel(self.table_frame, text="B", font=("Arial", 14, "bold"), text_color="#222222").grid(row=row_idx, column=2, padx=10, pady=5)
            ctk.CTkLabel(self.table_frame, text="C", font=("Arial", 14, "bold"), text_color="#222222").grid(row=row_idx, column=3, padx=10, pady=5)
            ctk.CTkLabel(self.table_frame, text="D", font=("Arial", 14, "bold"), text_color="#222222").grid(row=row_idx, column=4, padx=10, pady=5)
            ctk.CTkLabel(self.table_frame, text="Jawaban", font=("Arial", 14, "bold"), text_color="#222222").grid(row=row_idx, column=5, padx=10, pady=5)
            ctk.CTkLabel(self.table_frame, text="Penjelasan", font=("Arial", 14, "bold"), text_color="#222222").grid(row=row_idx, column=6, padx=10, pady=5)
            ctk.CTkLabel(self.table_frame, text="Aksi", font=("Arial", 14, "bold"), text_color="#222222").grid(row=row_idx, column=7, padx=10, pady=5)
            row_idx += 1
            soal_materi = [s for s in soal_list if s[1] == id_materi]
            if not soal_materi:
                ctk.CTkLabel(self.table_frame, text="Belum ada soal.", font=("Arial", 12), text_color="gray").grid(row=row_idx, column=0, padx=10, pady=5, columnspan=8)
                row_idx += 1
            else:
                for id_soal, _, question, a, b, c, d, correct, explanation in soal_materi:
                    ctk.CTkLabel(self.table_frame, text=question, font=("Arial", 12), text_color="#222222", wraplength=300, anchor="w").grid(row=row_idx, column=0, sticky="w", padx=10, pady=5)
                    ctk.CTkLabel(self.table_frame, text=a, font=("Arial", 12), text_color="#222222").grid(row=row_idx, column=1, padx=10, pady=5)
                    ctk.CTkLabel(self.table_frame, text=b, font=("Arial", 12), text_color="#222222").grid(row=row_idx, column=2, padx=10, pady=5)
                    ctk.CTkLabel(self.table_frame, text=c, font=("Arial", 12), text_color="#222222").grid(row=row_idx, column=3, padx=10, pady=5)
                    ctk.CTkLabel(self.table_frame, text=d, font=("Arial", 12), text_color="#222222").grid(row=row_idx, column=4, padx=10, pady=5)
                    ctk.CTkLabel(self.table_frame, text=correct, font=("Arial", 12), text_color="#222222").grid(row=row_idx, column=5, padx=10, pady=5)
                    ctk.CTkLabel(self.table_frame, text=explanation, font=("Arial", 12), text_color="#222222", wraplength=200).grid(row=row_idx, column=6, padx=10, pady=5)
                    ctk.CTkButton(self.table_frame, text="Hapus", command=lambda id=id_soal: self.hapus_soal(id), fg_color="#c0392b", text_color="white").grid(row=row_idx, column=7, padx=2, pady=2, sticky="n")
                    ctk.CTkButton(self.table_frame, text="Edit", command=lambda id=id_soal: self.edit_soal(id), fg_color="#f39c12", text_color="white").grid(row=row_idx+1, column=7, padx=2, pady=2, sticky="s")
                    row_idx += 2

    def tambah_soal(self):
        # Arahkan ke screen input soal (GuruApp)
        from Screens.guru_screen import GuruApp
        self.destroy()
        GuruApp(self.user_id, previous_screen=self.previous_screen).mainloop()

    def edit_soal(self, soal_id):
        # Ambil data soal dari database
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT question, option_a, option_b, option_c, option_d, correct_answer, explanation FROM questions WHERE id=?", (soal_id,))
        soal = cursor.fetchone()
        conn.close()
        if not soal:
            return
        # Buat window popup untuk edit soal dengan ukuran 75% layar
        import tkinter as tk
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        popup_width = int(screen_width * 0.75)
        popup_height = int(screen_height * 0.75)
        popup = ctk.CTkToplevel(self)
        popup.title("Edit Soal")
        popup.geometry(f"{popup_width}x{popup_height}+{int((screen_width-popup_width)/2)}+{int((screen_height-popup_height)/2)}")
        ctk.CTkLabel(popup, text="Edit Soal", font=("Arial", 20, "bold"), text_color="#ff6600").pack(pady=10)
        entries = {}
        labels = [
            ("Pertanyaan", soal[0]),
            ("Pilihan A", soal[1]),
            ("Pilihan B", soal[2]),
            ("Pilihan C", soal[3]),
            ("Pilihan D", soal[4]),
            ("Jawaban Benar (A/B/C/D)", soal[5]),
            ("Penjelasan", soal[6])
        ]
        for i, (label, value) in enumerate(labels):
            ctk.CTkLabel(popup, text=label, font=("Arial", 14, "bold"), text_color="#b34700").pack(anchor="w", padx=60, pady=(18 if i==0 else 8, 2))
            entry = ctk.CTkEntry(popup, width=int(popup_width*0.7))
            entry.insert(0, value)
            entry.pack(padx=60, pady=2)
            entries[label] = entry
        status_label = ctk.CTkLabel(popup, text="", font=("Arial", 12), text_color="#b34700")
        status_label.pack(pady=10)
        def simpan_edit():
            q = entries["Pertanyaan"].get()
            a = entries["Pilihan A"].get()
            b = entries["Pilihan B"].get()
            c = entries["Pilihan C"].get()
            d = entries["Pilihan D"].get()
            correct = entries["Jawaban Benar (A/B/C/D)"].get()
            explanation = entries["Penjelasan"].get()
            if not all([q, a, b, c, d, correct]):
                status_label.configure(text="Semua field wajib diisi!", text_color="red")
                return
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("UPDATE questions SET question=?, option_a=?, option_b=?, option_c=?, option_d=?, correct_answer=?, explanation=? WHERE id=?",
                           (q, a, b, c, d, correct, explanation, soal_id))
            conn.commit()
            conn.close()
            status_label.configure(text="Soal berhasil diupdate!", text_color="green")
            self.load_soal()
            popup.destroy()
        ctk.CTkButton(popup, text="Simpan Perubahan", command=simpan_edit, fg_color="#ff6600", hover_color="#b34700", text_color="white").pack(pady=20)
        ctk.CTkButton(popup, text="Batal", command=popup.destroy, fg_color="#888888", text_color="white").pack()

    def hapus_soal(self, soal_id):
        # TODO: Implementasi hapus soal
        pass

    def back_to_previous(self):
        self.destroy()
        if self.previous_screen:
            self.previous_screen.deiconify()
