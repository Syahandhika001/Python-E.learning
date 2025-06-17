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

class DashboardSoal(ctk.CTk):
    def __init__(self, user_id, previous_screen=None):
        super().__init__()
        self.title("Dashboard Guru")
        self.set_fullscreen_windowed()
        self.user_id = user_id
        self.previous_screen = previous_screen  # Menyimpan referensi ke layar sebelumnya
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
        # Card utama
        card = ctk.CTkFrame(self.gradient, fg_color="#f2f2f2", corner_radius=16)
        card.place(relx=0.5, rely=0.5, relwidth=0.7, relheight=0.7, anchor="center")
        # Judul
        ctk.CTkLabel(card, text="Dashboard Guru", font=("Arial", 32, "bold"), text_color="#ff6600").place(relx=0.5, rely=0.1, anchor="center")
        # Tombol Kelola Materi
        ctk.CTkButton(card, text="Kelola Materi", command=self.open_materi_screen, fg_color="#ff6600", hover_color="#b34700", text_color="white", font=("Arial", 18, "bold")).place(relx=0.2, rely=0.4, relwidth=0.22, relheight=0.13)
        # Tombol Kelola Bahan Ajar
        ctk.CTkButton(card, text="Kelola Bahan Ajar", command=self.open_bahan_ajar_screen, fg_color="#ff6600", hover_color="#b34700", text_color="white", font=("Arial", 18, "bold")).place(relx=0.4, rely=0.6, relwidth=0.22, relheight=0.13)
        # Tombol Kelola Soal (langsung ke GuruApp)
        ctk.CTkButton(card, text="Kelola Soal", command=self.open_guru_screen, fg_color="#ff6600", hover_color="#b34700", text_color="white", font=("Arial", 18, "bold")).place(relx=0.6, rely=0.4, relwidth=0.22, relheight=0.13)
        # Tombol Kembali ke Login
        ctk.CTkButton(card, text="Kembali", command=self.exit_to_login, fg_color="#b34700", hover_color="#ff6600", text_color="white", font=("Arial", 16, "bold")).place(relx=0.9, rely=0.9, relwidth=0.12, relheight=0.09, anchor="center")

    def open_materi_screen(self):
        from Screens.materi_screen import MateriScreen
        self.withdraw()
        materi_screen = MateriScreen(self.user_id, previous_screen=self)
        materi_screen.mainloop()

    def open_bahan_ajar_screen(self):
        from Screens.bahan_ajar_screen import BahanAjarScreen
        self.withdraw()
        bahan_ajar_screen = BahanAjarScreen(self.user_id, previous_screen=self)
        bahan_ajar_screen.mainloop()

    def open_guru_screen(self):
        from Screens.guru_screen import GuruApp  # Mengarahkan ke input soal (Guru)
        self.withdraw()
        guru_app = GuruApp(self.user_id, previous_screen=self)
        guru_app.mainloop()

    def exit_to_login(self):
        from Screens.login_screen import LoginApp
        self.destroy()
        login_app = LoginApp()
        login_app.mainloop()
