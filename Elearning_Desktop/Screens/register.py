import customtkinter as ctk
from db import register_user

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class RegisterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Halaman Registrasi")
        self.geometry("300x330")

        self.label = ctk.CTkLabel(self, text="Daftar Akun Baru")
        self.label.pack(pady=10)

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=10)

        self.role_entry = ctk.CTkEntry(self, placeholder_text="Role (misal: user)")
        self.role_entry.pack(pady=10)

        self.register_button = ctk.CTkButton(self, text="Daftar", command=self.register)
        self.register_button.pack(pady=20)

        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.pack()

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_entry.get() or "user"

        if username and password:
            success = register_user(username, password, role)
            if success:
                self.status_label.configure(text="Registrasi berhasil!", text_color="green")
            else:
                self.status_label.configure(text="Username sudah digunakan!", text_color="red")
        else:
            self.status_label.configure(text="Isi semua data!", text_color="orange")

if __name__ == "__main__":
    app = RegisterApp()
    app.mainloop()
