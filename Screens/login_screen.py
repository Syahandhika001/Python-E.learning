import tkinter as tk
import customtkinter as ctk
from db import connect_db
from screeninfo import get_monitors



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

class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("LoginScreen")
        self.configure(bg="#7f2100")  # Set background utama sama dengan warna gradient paling luar
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
        # Gradient background
        self.gradient = GradientFrame(self, color1="#e65c00", color2="#7f2100")
        self.gradient.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Card (rounded frame)
        self.card = ctk.CTkFrame(self.gradient, fg_color="#dddddd", corner_radius=12)
        self.card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.58, relheight=0.68)

        # SIGN IN Title
        ctk.CTkLabel(self.card, text="SIGN IN", font=("Arial", 48, "bold"), text_color="#ff8800").place(relx=0.5, rely=0.13, anchor="center")

        # Username Entry
        self.username_entry = ctk.CTkEntry(self.card, placeholder_text="Masukkan User", fg_color="#e6d8a3", text_color="#7f6a2a", font=("Arial", 16, "bold"))
        self.username_entry.place(relx=0.5, rely=0.28, relwidth=0.75, relheight=0.11, anchor="center")

        # Password Entry
        self.password_entry = ctk.CTkEntry(self.card, placeholder_text="Kata Sandi", show="*", fg_color="#e6d8a3", text_color="#7f6a2a", font=("Arial", 16, "bold"))
        self.password_entry.place(relx=0.5, rely=0.43, relwidth=0.75, relheight=0.11, anchor="center")

        # Login Button
        ctk.CTkButton(self.card, text="Login", command=self.login, fg_color="#e67c4a", hover_color="#d35400", text_color="#5a1d0a", font=("Arial", 22, "bold"), corner_radius=20).place(relx=0.5, rely=0.60, relwidth=0.4, relheight=0.11, anchor="center")

        # Status Label
        self.status_label = ctk.CTkLabel(self.card, text="", font=("Arial", 14))
        self.status_label.place(relx=0.5, rely=0.73, anchor="center")

        # Register Link
        label_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        label_frame.place(relx=0.5, rely=0.87, anchor="center")
        ctk.CTkLabel(label_frame, text="Belum Punya Akun? ", font=("Arial", 16, "bold"), text_color="#5a1d0a").pack(side="left")
        ctk.CTkButton(label_frame, text="Daftar Sekarang", command=self.open_register, fg_color="transparent", text_color="#ff8800", hover_color="#ffe0b2", font=("Arial", 16, "bold"), width=10, height=10, border_width=0).pack(side="left")

    def open_register(self):
        from Screens.register_screen import RegisterApp
        self.destroy()
        register_app = RegisterApp()
        register_app.mainloop()

    def login(self):
        from Screens.guru_screen import GuruApp
        from Screens.siswa_screen import SiswaApp
        from Screens.dashboard_soal import DashboardSoal
        # from Screens.dashboard_nilai import DashboardNilai  # ← Tidak dipakai lagi
        from Screens.siswa_dashboard import SiswaDashboard   # ← Tambahkan ini

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
                    # Ganti dari DashboardNilai ke SiswaDashboard
                    SiswaDashboard(user_id, previous_screen=self).mainloop()
            else:
                self.status_label.configure(text="Username atau Password salah!", text_color="red")
        else:
            self.status_label.configure(text="Isi semua data!", text_color="orange")
