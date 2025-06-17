import customtkinter as ctk
from db import connect_db
from screeninfo import get_monitors

class DashboardSoal(ctk.CTk):
    def __init__(self, user_id, previous_screen=None):
        super().__init__()
        self.title("Dashboard Guru")
        self.set_fullscreen_windowed()
        self.user_id = user_id
        self.previous_screen = previous_screen  # Menyimpan referensi ke layar sebelumnya
        self.create_widgets()

    def set_fullscreen_windowed(self):
        monitor = get_monitors()[0]
        screen_width = monitor.width
        screen_height = monitor.height
        self.geometry(f"{screen_width}x{screen_height}+0+0")

    def create_widgets(self):
        # Judul
        ctk.CTkLabel(self, text="Dashboard Guru", font=("Arial", 28)).place(relx=0.5, rely=0.1, anchor="center")

        # Tombol Kelola Materi
        ctk.CTkButton(
            self, text="Kelola Materi", command=self.open_materi_screen
        ).place(relx=0.2, rely=0.4, relwidth=0.2, relheight=0.12)

        # Tombol Kelola Bahan Ajar
        ctk.CTkButton(
            self, text="Kelola Bahan Ajar", command=self.open_bahan_ajar_screen
        ).place(relx=0.4, rely=0.6, relwidth=0.2, relheight=0.12)

        # Tombol Kelola Soal (langsung ke GuruApp)
        ctk.CTkButton(
            self, text="Kelola Soal", command=self.open_guru_screen
        ).place(relx=0.6, rely=0.4, relwidth=0.2, relheight=0.12)

        # Tombol Kembali ke Login
        ctk.CTkButton(
            self, text="Kembali", command=self.exit_to_login
        ).place(relx=0.9, rely=0.9, relwidth=0.08, relheight=0.06)

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
