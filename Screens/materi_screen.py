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

class MateriScreen(ctk.CTk):
    def __init__(self, user_id, previous_screen=None):
        super().__init__()
        self.title("MateriScreen")
        self.set_fullscreen_windowed()
        self.user_id = user_id
        self.previous_screen = previous_screen
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
        card = ctk.CTkFrame(self.gradient, fg_color="#f2f2f2", corner_radius=16)
        card.place(relx=0.5, rely=0.5, relwidth=0.8, relheight=0.8, anchor="center")
        ctk.CTkLabel(card, text="Daftar Materi", font=("Arial", 28, "bold"), text_color="#ff6600").place(relx=0.5, rely=0.08, anchor="center")
        self.table_frame = ctk.CTkFrame(card, fg_color="#fff7e6", corner_radius=8)
        self.table_frame.place(relx=0.5, rely=0.45, relwidth=0.9, relheight=0.5, anchor="center")
        self.load_materi()
        ctk.CTkLabel(card, text="Judul Materi:", font=("Arial", 14, "bold"), text_color="#b34700").place(relx=0.2, rely=0.8, anchor="w")
        self.judul_entry = ctk.CTkEntry(card, width=300, fg_color="#fff7e6", text_color="#222222")
        self.judul_entry.place(relx=0.3, rely=0.8, anchor="w")
        ctk.CTkLabel(card, text="Deskripsi:", font=("Arial", 14, "bold"), text_color="#b34700").place(relx=0.2, rely=0.85, anchor="w")
        self.deskripsi_entry = ctk.CTkEntry(card, width=300, fg_color="#fff7e6", text_color="#222222")
        self.deskripsi_entry.place(relx=0.3, rely=0.85, anchor="w")
        self.status_label = ctk.CTkLabel(card, text="", font=("Arial", 12), text_color="#b34700")
        self.status_label.place(relx=0.5, rely=0.93, anchor="center")
        ctk.CTkButton(card, text="Tambah/Update Materi", command=self.save_materi, fg_color="#ff6600", hover_color="#b34700", text_color="white", font=("Arial", 16, "bold")).place(relx=0.6, rely=0.8, relwidth=0.15, relheight=0.07)
        ctk.CTkButton(card, text="Hapus Materi", command=self.delete_materi, fg_color="#b34700", hover_color="#ff6600", text_color="white", font=("Arial", 16, "bold")).place(relx=0.8, rely=0.8, relwidth=0.15, relheight=0.07)
        ctk.CTkButton(card, text="Kembali", command=self.back_to_dashboard, fg_color="#b34700", hover_color="#ff6600", text_color="white", font=("Arial", 16, "bold")).place(relx=0.9, rely=0.95, relwidth=0.08, relheight=0.05)
        self.selected_id = None

    def load_materi(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, judul, deskripsi FROM materi")
        rows = cursor.fetchall()
        conn.close()
        # Header tabel dengan warna font gelap
        ctk.CTkLabel(self.table_frame, text="Judul", font=("Arial", 14, "bold"), text_color="#222222").grid(row=0, column=0, padx=10, pady=5)
        ctk.CTkLabel(self.table_frame, text="Deskripsi", font=("Arial", 14, "bold"), text_color="#222222").grid(row=0, column=1, padx=10, pady=5)
        for i, (id_materi, judul, deskripsi) in enumerate(rows, start=1):
            btn = ctk.CTkButton(self.table_frame, text=judul, command=lambda i=id_materi, j=judul, d=deskripsi: self.select_materi(i, j, d), anchor="w", fg_color="#2176ae", text_color="white", font=("Arial", 13, "bold"))
            btn.grid(row=i, column=0, sticky="w", padx=10, pady=5)
            ctk.CTkLabel(self.table_frame, text=deskripsi, anchor="w", text_color="#222222", font=("Arial", 12)).grid(row=i, column=1, sticky="w", padx=10, pady=5)

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
