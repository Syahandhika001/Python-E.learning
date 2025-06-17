import tkinter as tk
import customtkinter as ctk
from screeninfo import get_monitors
from db import connect_db


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


class RegisterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("RegisterScreen")
        self.configure(bg="#7f2100")
        self.set_fullscreen_windowed()
        self.create_widgets()

    def set_fullscreen_windowed(self):
        monitor = get_monitors()[0]
        screen_width = monitor.width
        screen_height = monitor.height
        self.geometry(f"{screen_width}x{screen_height}+0+0")

    def create_widgets(self):
        self.gradient = GradientFrame(self, color1="#e65c00", color2="#7f2100")
        self.gradient.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.card = ctk.CTkFrame(self.gradient, fg_color="#dddddd", corner_radius=12)
        self.card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.58, relheight=0.68)

        ctk.CTkLabel(self.card, text="Daftar Akun Baru", font=("Arial", 38, "bold"), text_color="#ff8800").place(relx=0.5, rely=0.12, anchor="center")

        self.username_entry = ctk.CTkEntry(self.card, placeholder_text="Nama Pengguna", fg_color="#f8e49c", text_color="#7f6a2a", font=("Arial", 16, "bold"))
        self.username_entry.place(relx=0.5, rely=0.28, relwidth=0.75, relheight=0.11, anchor="center")

        self.password_entry = ctk.CTkEntry(self.card, placeholder_text="Kata Sandi", show="*", fg_color="#f8e49c", text_color="#7f6a2a", font=("Arial", 16, "bold"))
        self.password_entry.place(relx=0.5, rely=0.43, relwidth=0.75, relheight=0.11, anchor="center")

        ctk.CTkLabel(self.card, text="Pilih Peran:", font=("Arial", 16, "bold"), text_color="#5a1d0a").place(relx=0.5, rely=0.57, anchor="center")

        self.role_combobox = ctk.CTkComboBox(self.card, values=["siswa", "guru"], font=("Arial", 16, "bold"),
                                             fg_color="#ff8844", dropdown_fg_color="#ffd8b0",
                                             dropdown_text_color="#5a1d0a", text_color="white", button_color="#cc5200")
        self.role_combobox.place(relx=0.5, rely=0.66, relwidth=0.5, relheight=0.1, anchor="center")
        self.role_combobox.set("siswa")

        self.status_label = ctk.CTkLabel(self.card, text="", font=("Arial", 14))
        self.status_label.place(relx=0.5, rely=0.78, anchor="center")

        ctk.CTkButton(self.card, text="Daftar", command=self.register,
                      fg_color="#ff8844", hover_color="#cc5200", text_color="white",
                      font=("Arial", 22, "bold"), corner_radius=20).place(
            relx=0.5, rely=0.89, relwidth=0.4, relheight=0.11, anchor="center")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_combobox.get()

        if username and password and role:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username=?", (username,))
            if cursor.fetchone():
                self.status_label.configure(text="Username sudah terdaftar!", text_color="red")
            else:
                cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                               (username, password, role))
                conn.commit()
                self.status_label.configure(text="Pendaftaran berhasil!", text_color="green")
                conn.close()
                # Setelah berhasil daftar, langsung ke login
                self.after(1000, self.kembali_ke_login)
                return
            conn.close()
        else:
            self.status_label.configure(text="Isi semua data!", text_color="orange")

    def kembali_ke_login(self):
        from Screens.login_screen import LoginApp
        self.destroy()
        login_app = LoginApp()
        login_app.mainloop()

