import customtkinter as ctk
from db import connect_db
from screeninfo import get_monitors
from Screens.siswa_bahan_ajar import SiswaBahanAjar
from Screens.siswa_kerjakan_soal import SiswaKerjakanSoal
import tkinter as tk

class GradientFrame(ctk.CTkFrame):
    def __init__(self, master, color1, color2, **kwargs):
        super().__init__(master, **kwargs)
        self.color1 = color1
        self.color2 = color2
        self.canvas = tk.Canvas(self, highlightthickness=0)
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

class SiswaDashboard(ctk.CTk):
    def __init__(self, user_id, previous_screen=None):
        super().__init__()
        self.user_id = user_id
        self.previous_screen = previous_screen
        self.title("Dashboard Materi")
        self.configure(bg="#7f2100")
        self.set_fullscreen()
        self.create_widgets()

    def set_fullscreen(self):
        monitor = get_monitors()[0]
        self.geometry(f"{monitor.width}x{monitor.height}+0+0")

    def create_widgets(self):
        # Gradient background
        self.gradient = GradientFrame(self, color1="#e65c00", color2="#7f2100")
        self.gradient.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Frame utama
        main_frame = ctk.CTkFrame(self.gradient, fg_color="#dddddd", corner_radius=12)
        main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.85)

        # Judul
        ctk.CTkLabel(main_frame, text="Dashboard Siswa", font=("Arial", 36, "bold"), text_color="#ff8800").pack(pady=20)

        # Frame scroll
        container = ctk.CTkScrollableFrame(main_frame, width=1000, height=500, fg_color="#f3e5ab")
        container.pack(padx=40, pady=10, fill="both", expand=True)

        # Ambil data materi
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, judul, deskripsi FROM materi")
        materi_list = cursor.fetchall()
        conn.close()

        if not materi_list:
            ctk.CTkLabel(container, text="Belum ada materi.", font=("Arial", 16), text_color="gray").pack(pady=20)
        else:
            for materi_id, judul, deskripsi in materi_list:
                # Kartu Materi
                card = ctk.CTkFrame(container, fg_color="#fff8dc", corner_radius=16)
                card.pack(padx=10, pady=15, fill="x")

                ctk.CTkLabel(card, text=judul, font=("Arial", 20, "bold"), text_color="#7f2100").pack(anchor="w", padx=15, pady=(12, 6))
                ctk.CTkLabel(card, text=deskripsi, font=("Arial", 14), text_color="#5a1d0a", wraplength=1000, justify="left").pack(anchor="w", padx=15, pady=(0, 10))

                # Tombol Aksi
                button_frame = ctk.CTkFrame(card, fg_color="transparent")
                button_frame.pack(anchor="e", padx=15, pady=(0, 15))

                ctk.CTkButton(button_frame, text="Detail", width=100, fg_color="#e67c4a", hover_color="#d35400", text_color="white",
                              font=("Arial", 14, "bold"), command=lambda mid=materi_id: self.open_bahan(mid)).pack(side="left", padx=5)
                ctk.CTkButton(button_frame, text="Kerjakan Soal", width=140, fg_color="#f39c12", hover_color="#e67e22", text_color="white",
                              font=("Arial", 14, "bold"), command=lambda mid=materi_id: self.open_soal(mid)).pack(side="left", padx=5)

        # Tombol kembali
        ctk.CTkButton(main_frame, text="Kembali", command=self.go_back, fg_color="#7f2100", hover_color="#a23c00", text_color="white",
                      font=("Arial", 16, "bold"), width=120).pack(pady=25)

    def open_bahan(self, materi_id):
        self.withdraw()
        SiswaBahanAjar(self.user_id, materi_id, previous_screen=self).mainloop()

    def open_soal(self, materi_id):
        self.withdraw()
        SiswaKerjakanSoal(self.user_id, materi_id, previous_screen=self).mainloop()

    def go_back(self):
        self.destroy()
        if self.previous_screen:
            self.previous_screen.deiconify()
