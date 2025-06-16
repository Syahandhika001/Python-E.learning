import customtkinter as ctk
from db import connect_db
from screeninfo import get_monitors

class MateriScreen(ctk.CTk):
    def __init__(self, user_id, previous_screen=None):
        super().__init__()
        self.title("MateriScreen")
        self.set_fullscreen_windowed()
        self.user_id = user_id
        self.previous_screen = previous_screen
        self.create_widgets()

    def set_fullscreen_windowed(self):
        monitor = get_monitors()[0]
        screen_width = monitor.width
        screen_height = monitor.height
        self.geometry(f"{screen_width}x{screen_height}+0+0")

    def create_widgets(self):
        ctk.CTkLabel(self, text="Daftar Materi", font=("Arial", 24)).place(relx=0.5, rely=0.05, anchor="center")
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.place(relx=0.5, rely=0.4, relwidth=0.8, relheight=0.5, anchor="center")
        self.load_materi()

        # Form tambah/edit
        ctk.CTkLabel(self, text="Judul Materi:").place(relx=0.2, rely=0.8, anchor="w")
        self.judul_entry = ctk.CTkEntry(self, width=300)
        self.judul_entry.place(relx=0.3, rely=0.8, anchor="w")
        ctk.CTkLabel(self, text="Deskripsi:").place(relx=0.2, rely=0.85, anchor="w")
        self.deskripsi_entry = ctk.CTkEntry(self, width=300)
        self.deskripsi_entry.place(relx=0.3, rely=0.85, anchor="w")
        self.status_label = ctk.CTkLabel(self, text="", font=("Arial", 12))
        self.status_label.place(relx=0.5, rely=0.93, anchor="center")
        ctk.CTkButton(self, text="Tambah/Update Materi", command=self.save_materi).place(relx=0.6, rely=0.8, relwidth=0.15, relheight=0.07)
        ctk.CTkButton(self, text="Hapus Materi", command=self.delete_materi).place(relx=0.8, rely=0.8, relwidth=0.15, relheight=0.07)
        ctk.CTkButton(self, text="Kembali", command=self.back_to_dashboard).place(relx=0.9, rely=0.95, relwidth=0.08, relheight=0.05)
        self.selected_id = None

    def load_materi(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, judul, deskripsi FROM materi")
        rows = cursor.fetchall()
        conn.close()
        ctk.CTkLabel(self.table_frame, text="Judul", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=10, pady=5)
        ctk.CTkLabel(self.table_frame, text="Deskripsi", font=("Arial", 14, "bold")).grid(row=0, column=1, padx=10, pady=5)
        for i, (id_materi, judul, deskripsi) in enumerate(rows, start=1):
            btn = ctk.CTkButton(self.table_frame, text=judul, command=lambda i=id_materi, j=judul, d=deskripsi: self.select_materi(i, j, d), anchor="w")
            btn.grid(row=i, column=0, sticky="w", padx=10, pady=5)
            ctk.CTkLabel(self.table_frame, text=deskripsi, anchor="w").grid(row=i, column=1, sticky="w", padx=10, pady=5)

    def select_materi(self, id_materi, judul, deskripsi):
        self.selected_id = id_materi
        self.judul_entry.delete(0, 'end')
        self.judul_entry.insert(0, judul)
        self.deskripsi_entry.delete(0, 'end')
        self.deskripsi_entry.insert(0, deskripsi)
        self.status_label.configure(text=f"Edit Materi ID: {id_materi}", text_color="orange")

    def save_materi(self):
        judul = self.judul_entry.get()
        deskripsi = self.deskripsi_entry.get()
        if not judul:
            self.status_label.configure(text="Judul tidak boleh kosong!", text_color="red")
            return
        conn = connect_db()
        cursor = conn.cursor()
        if self.selected_id:
            cursor.execute("UPDATE materi SET judul=?, deskripsi=? WHERE id=?", (judul, deskripsi, self.selected_id))
            self.status_label.configure(text="Materi diperbarui!", text_color="green")
        else:
            cursor.execute("INSERT INTO materi (judul, deskripsi) VALUES (?, ?)", (judul, deskripsi))
            self.status_label.configure(text="Materi ditambahkan!", text_color="green")
        conn.commit()
        conn.close()
        self.selected_id = None
        self.judul_entry.delete(0, 'end')
        self.deskripsi_entry.delete(0, 'end')
        self.load_materi()

    def delete_materi(self):
        if not self.selected_id:
            self.status_label.configure(text="Pilih materi yang akan dihapus!", text_color="red")
            return
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM materi WHERE id=?", (self.selected_id,))
        conn.commit()
        conn.close()
        self.status_label.configure(text="Materi dihapus!", text_color="green")
        self.selected_id = None
        self.judul_entry.delete(0, 'end')
        self.deskripsi_entry.delete(0, 'end')
        self.load_materi()

    def back_to_dashboard(self):
        self.destroy()
        if self.previous_screen:
            self.previous_screen.deiconify()
