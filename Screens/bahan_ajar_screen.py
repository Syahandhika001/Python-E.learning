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

class BahanAjarScreen(ctk.CTk):
    def __init__(self, user_id, previous_screen=None):
        super().__init__()
        self.title("BahanAjarScreen")
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
        ctk.CTkLabel(card, text="Daftar Bahan Ajar", font=("Arial", 28, "bold"), text_color="#ff6600").place(relx=0.5, rely=0.08, anchor="center")
        self.table_frame = ctk.CTkFrame(card, fg_color="#fff7e6", corner_radius=8)
        self.table_frame.place(relx=0.5, rely=0.45, relwidth=0.9, relheight=0.5, anchor="center")
        self.load_bahan_ajar()
        ctk.CTkLabel(card, text="Pilih Materi:", font=("Arial", 14, "bold"), text_color="#b34700").place(relx=0.2, rely=0.8, anchor="w")
        self.materi_option = ctk.CTkOptionMenu(card, values=self.get_materi_list(), fg_color="#ff6600", text_color="white")
        self.materi_option.place(relx=0.3, rely=0.8, anchor="w")
        ctk.CTkLabel(card, text="Nama Bahan:", font=("Arial", 14, "bold"), text_color="#b34700").place(relx=0.2, rely=0.85, anchor="w")
        self.nama_entry = ctk.CTkEntry(card, width=300, fg_color="#fff7e6", text_color="#222222")
        self.nama_entry.place(relx=0.3, rely=0.85, anchor="w")
        ctk.CTkLabel(card, text="File Path:", font=("Arial", 14, "bold"), text_color="#b34700").place(relx=0.2, rely=0.9, anchor="w")
        self.file_entry = ctk.CTkEntry(card, width=300, fg_color="#fff7e6", text_color="#222222")
        self.file_entry.place(relx=0.3, rely=0.9, anchor="w")
        self.status_label = ctk.CTkLabel(card, text="", font=("Arial", 12), text_color="#b34700")
        self.status_label.place(relx=0.5, rely=0.95, anchor="center")
        ctk.CTkButton(card, text="Tambah/Update Bahan", command=self.save_bahan, fg_color="#ff6600", hover_color="#b34700", text_color="white", font=("Arial", 16, "bold")).place(relx=0.6, rely=0.85, relwidth=0.15, relheight=0.07)
        ctk.CTkButton(card, text="Hapus Bahan", command=self.delete_bahan, fg_color="#b34700", hover_color="#ff6600", text_color="white", font=("Arial", 16, "bold")).place(relx=0.8, rely=0.85, relwidth=0.15, relheight=0.07)
        ctk.CTkButton(card, text="Kembali", command=self.back_to_dashboard, fg_color="#b34700", hover_color="#ff6600", text_color="white", font=("Arial", 16, "bold")).place(relx=0.9, rely=0.95, relwidth=0.08, relheight=0.05)
        self.selected_id = None

    def get_materi_list(self):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, judul FROM materi")
        rows = cursor.fetchall()
        conn.close()
        return [f"{id_materi} - {judul}" for id_materi, judul in rows] if rows else ["-"]

    def load_bahan_ajar(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT bahan_ajar.id, materi.judul, bahan_ajar.nama_bahan, bahan_ajar.file_path FROM bahan_ajar JOIN materi ON bahan_ajar.materi_id = materi.id")
        rows = cursor.fetchall()
        conn.close()
        # Header tabel dengan warna font gelap
        ctk.CTkLabel(self.table_frame, text="Materi", font=("Arial", 14, "bold"), text_color="#222222").grid(row=0, column=0, padx=10, pady=5)
        ctk.CTkLabel(self.table_frame, text="Nama Bahan", font=("Arial", 14, "bold"), text_color="#222222").grid(row=0, column=1, padx=10, pady=5)
        ctk.CTkLabel(self.table_frame, text="File", font=("Arial", 14, "bold"), text_color="#222222").grid(row=0, column=2, padx=10, pady=5)
        for i, (id_bahan, judul, nama, file_path) in enumerate(rows, start=1):
            btn = ctk.CTkButton(self.table_frame, text=nama, command=lambda i=id_bahan, m=judul, n=nama, f=file_path: self.select_bahan(i, m, n, f), anchor="w", fg_color="#2176ae", text_color="white", font=("Arial", 13, "bold"))
            btn.grid(row=i, column=1, sticky="w", padx=10, pady=5)
            ctk.CTkLabel(self.table_frame, text=judul, anchor="w", text_color="#222222", font=("Arial", 12)).grid(row=i, column=0, sticky="w", padx=10, pady=5)
            ctk.CTkLabel(self.table_frame, text=file_path, anchor="w", text_color="#222222", font=("Arial", 12)).grid(row=i, column=2, sticky="w", padx=10, pady=5)

    def select_bahan(self, id_bahan, judul, nama, file_path):
        self.selected_id = id_bahan
        self.nama_entry.delete(0, 'end')
        self.nama_entry.insert(0, nama)
        self.file_entry.delete(0, 'end')
        self.file_entry.insert(0, file_path)
        self.status_label.configure(text=f"Edit Bahan ID: {id_bahan}", text_color="orange")
        # Set materi_option sesuai judul
        for val in self.materi_option.cget('values'):
            if judul in val:
                self.materi_option.set(val)
                break

    def save_bahan(self):
        nama = self.nama_entry.get()
        file_path = self.file_entry.get()
        materi_val = self.materi_option.get()
        if not nama or not materi_val or materi_val == "-":
            self.status_label.configure(text="Nama bahan & materi wajib diisi!", text_color="red")
            return
        materi_id = int(materi_val.split(' - ')[0])
        conn = connect_db()
        cursor = conn.cursor()
        if self.selected_id:
            cursor.execute("UPDATE bahan_ajar SET materi_id=?, nama_bahan=?, file_path=? WHERE id=?", (materi_id, nama, file_path, self.selected_id))
            self.status_label.configure(text="Bahan ajar diperbarui!", text_color="green")
        else:
            cursor.execute("INSERT INTO bahan_ajar (materi_id, nama_bahan, file_path) VALUES (?, ?, ?)", (materi_id, nama, file_path))
            self.status_label.configure(text="Bahan ajar ditambahkan!", text_color="green")
        conn.commit()
        conn.close()
        self.selected_id = None
        self.nama_entry.delete(0, 'end')
        self.file_entry.delete(0, 'end')
        self.load_bahan_ajar()
        self.materi_option.configure(values=self.get_materi_list())

    def delete_bahan(self):
        if not self.selected_id:
            self.status_label.configure(text="Pilih bahan ajar yang akan dihapus!", text_color="red")
            return
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM bahan_ajar WHERE id=?", (self.selected_id,))
        conn.commit()
        conn.close()
        self.status_label.configure(text="Bahan ajar dihapus!", text_color="green")
        self.selected_id = None
        self.nama_entry.delete(0, 'end')
        self.file_entry.delete(0, 'end')
        self.load_bahan_ajar()
        self.materi_option.configure(values=self.get_materi_list())

    def back_to_dashboard(self):
        self.destroy()
        if self.previous_screen:
            self.previous_screen.deiconify()
