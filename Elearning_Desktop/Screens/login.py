import customtkinter as ctk
from tkinter import messagebox
from db import connect_db

class LoginScreen(ctk.CTkFrame):
    def __init__(self, parent, login_callback):
        super().__init__(parent)
        self.login_callback = login_callback

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=10)

        self.login_button = ctk.CTkButton(self, text="Login", command=self.handle_login)
        self.login_button.pack(pady=10)

        self.register_button = ctk.CTkButton(self, text="Register", command=self.handle_register)
        self.register_button.pack(pady=5)

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
        result = cursor.fetchone()
        conn.close()

        if result:
            role = result[0]
            self.login_callback(role)
        else:
            messagebox.showerror("Login Gagal", "Username atau password salah")

    def handle_register(self):
        from screens.register_screen import RegisterScreen
        self.master.clear_widgets()
        RegisterScreen(self.master).pack(expand=True, fill="both")
