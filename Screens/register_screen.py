import customtkinter as ctk
from db import register_user
from screeninfo import get_monitors


class RegisterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Halaman Registrasi")
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
        ctk.CTkLabel(self, text="Daftar Akun Baru", font=("Arial", 24)).place(relx=0.5, rely=0.1, anchor="center")

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Nama Pengguna")
        self.username_entry.place(relx=0.5, rely=0.2, relwidth=0.6, relheight=0.07, anchor="center")

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Kata Sandi", show="*")
        self.password_entry.place(relx=0.5, rely=0.3, relwidth=0.6, relheight=0.07, anchor="center")

        ctk.CTkLabel(self, text="Pilih Peran:", font=("Arial", 14)).place(relx=0.5, rely=0.4, anchor="center")
        self.role_option = ctk.CTkOptionMenu(self, values=["siswa", "guru"])
        self.role_option.set("siswa")
        self.role_option.place(relx=0.5, rely=0.45, relwidth=0.4, relheight=0.07, anchor="center")

        ctk.CTkButton(self, text="Daftar", command=self.register).place(relx=0.5, rely=0.6, relwidth=0.3, relheight=0.07, anchor="center")
        self.status_label = ctk.CTkLabel(self, text="", font=("Arial", 14))
        self.status_label.place(relx=0.5, rely=0.7, anchor="center")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_option.get()

        if username and password and role:
            success = register_user(username, password, role)
            if success:
                self.status_label.configure(text="Registrasi berhasil!", text_color="green")
                self.after(1000, self.redirect_to_login)  # Redirect after 1 second
            else:
                self.status_label.configure(text="Username sudah digunakan!", text_color="red")
        else:
            self.status_label.configure(text="Isi semua data!", text_color="orange")

    def redirect_to_login(self):
        from Screens.login_screen import LoginApp
        self.destroy()
        login_app = LoginApp()
        login_app.mainloop()
