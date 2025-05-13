import customtkinter as ctk
from db import connect_db
from screeninfo import get_monitors



class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Halaman Login")
        self.set_fullscreen_windowed()
        self.create_widgets()
    
    def set_fullscreen_windowed(self):
        # Dapatkan resolusi layar utama
        monitor = get_monitors()[0]
        screen_width = monitor.width
        screen_height = monitor.height

        # Atur ukuran jendela agar sesuai dengan resolusi layar
        self.geometry(f"{screen_width}x{screen_height}+0+0")

    def create_widgets(self):
        ctk.CTkLabel(self, text="Masuk Akun", font=("Arial", 24)).place(relx=0.5, rely=0.1, anchor="center")

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.username_entry.place(relx=0.5, rely=0.2, relwidth=0.6, relheight=0.07, anchor="center")

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.place(relx=0.5, rely=0.3, relwidth=0.6, relheight=0.07, anchor="center")

        ctk.CTkButton(self, text="Login", command=self.login).place(relx=0.5, rely=0.4, relwidth=0.3, relheight=0.07, anchor="center")

        self.status_label = ctk.CTkLabel(self, text="", font=("Arial", 14))
        self.status_label.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkButton(self, text="Belum punya akun? Daftar di sini",
                      command=self.open_register, fg_color="transparent",
                      text_color="blue", hover_color="#ccc", border_width=1).place(relx=0.5, rely=0.6, relwidth=0.3, relheight=0.07, anchor="center")

    def open_register(self):
        from Screens.register_screen import RegisterApp
        self.destroy()
        register_app = RegisterApp()
        register_app.mainloop()

    def login(self):
        from Screens.guru_screen import GuruApp
        from Screens.siswa_screen import SiswaApp
        from Screens.dashboard_soal import DashboardSoal
        from Screens.dashboard_nilai import DashboardNilai

        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            user = cursor.fetchone()
            conn.close()

            if user:
                user_id, role = user[0], user[3]
                self.withdraw()  # Sembunyikan screen login
                if role == "guru":
                    DashboardSoal(user_id, previous_screen=self).mainloop()
                else:
                    DashboardNilai(user_id, previous_screen=self).mainloop()
            else:
                self.status_label.configure(text="Username atau Password salah!", text_color="red")
        else:
            self.status_label.configure(text="Isi semua data!", text_color="orange")
